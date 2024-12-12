from scapy.all import *
import threading
from collections import defaultdict
import time
from gmail  import *

# Configuration des seuils
BRUTE_FORCE_THRESHOLD = 10  # Tentatives par IP sur le même port
DDOS_THRESHOLD = 500        # Nombre de requêtes d'une IP en moins de 10 secondes
SCAN_THRESHOLD = 10         # Nombre de ports scannés par une même IP

INTERVAL = 20

CONNECTION_PORT = 3000
ADMIN = ["jules.leroquais@epita.fr", "emna.gharbi@epita.fr", "azza.mani@epita.fr"]

ignore_src = [3000, 8080, 80]

ddos_ip_src = []
brute_force_ip_src = []
port_scan_ip_src = []

# Données pour suivre l'activité réseau
brute_force_tracker = defaultdict(list)
ddos_tracker = defaultdict(list)
port_scan_tracker = defaultdict(set)

def detect_brute_force(packet):
    """Détecte les attaques de brute force sur un port spécifique."""
    src_ip = packet[IP].src
    dst_port = packet[TCP].dport

    
    #check that is trying to on a connection

    if not packet.haslayer(Raw):
        return
    
    payload = packet[Raw].load.decode(errors="ignore")
    if not "POST" in payload:
        return
    

    now = time.time()
    brute_force_tracker[(src_ip, dst_port)].append(now)

    if (src_ip, dst_port) in brute_force_ip_src:
        return
    
    if len(brute_force_tracker[(src_ip, dst_port)]) > BRUTE_FORCE_THRESHOLD:
        brute_force_ip_src.append((src_ip, dst_port))

def detect_ddos(packet):
    """Détecte les attaques DDoS à partir d'une IP source."""

    if not packet.haslayer(Raw):
        return
    #print(packet[Raw].load)
    src_ip = packet[IP].src
    now = time.time()
    ddos_tracker[src_ip].append(now)

    if src_ip in ddos_ip_src:
        return
    
    if len(ddos_tracker[src_ip]) > DDOS_THRESHOLD:
        ddos_ip_src.append(src_ip)

def detect_port_scan(src_ip, dst_port):
    """Détecte les scans de ports en surveillant les connexions à plusieurs ports."""
    if not (dst_port in port_scan_tracker[src_ip]):
        port_scan_tracker[src_ip].add(dst_port)

    if src_ip in port_scan_ip_src:
        return
    
    if len(port_scan_tracker[src_ip]) > SCAN_THRESHOLD:
        port_scan_ip_src.append(src_ip)




def clear_list():
    ddos_ip_src.clear()
    brute_force_ip_src.clear()
    port_scan_ip_src.clear()

    # Données pour suivre l'activité réseau
    brute_force_tracker.clear()
    ddos_tracker.clear()
    port_scan_tracker.clear()

def check_list():
    alert = False
    txt =""
    if len(ddos_ip_src) > 0:
        alert = True
        txt = "DDoS detected:\n"
        for ip in ddos_ip_src:
            txt += f"\tIP {ip} sent {len(ddos_tracker[ip])} packets\n"
            print(f"[ALERTE] DDoS détecté : IP {ip} a envoyé {len(ddos_tracker[ip])}")

    if len(brute_force_ip_src) > 0:
        if alert:
            txt += "\nBrute Force detected:\n"
        else:
            alert = True
        for (ip, port) in brute_force_ip_src:
            txt += f"\tIP {ip} tried {len(brute_force_tracker[(ip, port)])} to connect over the port {port}\n"
            print(f"[ALERTE] Brute force détecté : IP {ip} a essayé {len(brute_force_tracker[(ip, port)])} sur le port {port}")
    if len(port_scan_ip_src) > 0:
        if alert:
            txt += "\nPort Scan detected:\n"
        else:
            alert = True
    for ip in port_scan_ip_src:
        txt += f"\tIP {ip} scanned {len(port_scan_tracker[ip])} ports\n"
        print(f"[ALERTE] Scan de ports détecté : IP {ip} a scanné {len(port_scan_tracker[ip])} ports")
    if alert:
        for email in ADMIN:
            envoyer_email_gmail(email, "[ALERT] NDIS", txt)

    clear_list()

def run_in_background():
    def loop():
        while True:
            check_list()
            time.sleep(INTERVAL)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()


def packet_handler(packet):
    """Traite les paquets capturés pour détecter des activités suspectes."""
    if IP in packet:
        src_ip = packet[IP].src
        if TCP in packet:
            dst_port = packet[TCP].dport
            if packet[TCP].sport in ignore_src:
                return
            # Détection brute force
            detect_brute_force(packet)

            # Détection DDoS
            detect_ddos(packet)

            # Détection scan de ports
            detect_port_scan(src_ip, dst_port)

if __name__ == "__main__":
    print("[INFO] Détection en cours... Appuyez sur CTRL+C pour arrêter.")
    # Capture des paquets sur l'interface réseau
    run_in_background()
    sniff(iface="lo", prn=packet_handler, filter="tcp", store=0)
    
