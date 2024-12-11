from scapy.all import *
import threading
from collections import defaultdict
import time

# Configuration des seuils
BRUTE_FORCE_THRESHOLD = 10  # Tentatives par IP sur le même port
DDOS_THRESHOLD = 5000       # Nombre de requêtes d'une IP en moins de 10 secondes
SCAN_THRESHOLD = 100         # Nombre de ports scannés par une même IP


CONNECTION_PORT = 3000

ignore_src = [3000, 8080, 80]

ddos_ip_src = []
brute_force_ip_src = []
port_scan_ip_src = []

# Données pour suivre l'activité réseau
brute_force_tracker = defaultdict(list)
ddos_tracker = defaultdict(list)
port_scan_tracker = defaultdict(set)

clear = [int(time.time())]
def detect_brute_force(packet):
    """Détecte les attaques de brute force sur un port spécifique."""
    src_ip = packet[IP].src
    if src_ip in brute_force_ip_src:
        return
    dst_port = packet[TCP].dport

    #check that is trying to on a connection

    if not packet.haslayer(TCP) or not packet.haslayer(Raw):
        return
    
    payload = packet[Raw].load.decode(errors="ignore")
    if not "POST" in payload:
        return

    now = time.time()
    brute_force_tracker[(src_ip, dst_port)].append(now)

    # Garder seulement les timestamps récents
    brute_force_tracker[(src_ip, dst_port)] = [
        t for t in brute_force_tracker[(src_ip, dst_port)] if now - t < 10
    ]

    if len(brute_force_tracker[(src_ip, dst_port)]) > BRUTE_FORCE_THRESHOLD:
        print(f"[ALERTE] Brute force détecté : IP {src_ip} cible le port {dst_port}")
        brute_force_ip_src.append(src_ip)

def detect_ddos(src_ip):
    """Détecte les attaques DDoS à partir d'une IP source."""
    if src_ip in ddos_ip_src:
        return
    now = time.time()
    ddos_tracker[src_ip].append(now)

    # Garder seulement les timestamps récents
    ddos_tracker[src_ip] = [t for t in ddos_tracker[src_ip] if now - t < 10]

    if len(ddos_tracker[src_ip]) > DDOS_THRESHOLD:
        print(f"[ALERTE] DDoS détecté : IP {src_ip} envoie un grand nombre de requêtes")
        ddos_ip_src.append(src_ip)

def detect_port_scan(src_ip, dst_port):
    """Détecte les scans de ports en surveillant les connexions à plusieurs ports."""
    if src_ip in port_scan_ip_src:
        return
    if not (dst_port in port_scan_tracker[src_ip]):
        port_scan_tracker[src_ip].add(dst_port)

    if len(port_scan_tracker[src_ip]) > SCAN_THRESHOLD:
        print(f"[ALERTE] Scan de ports détecté : IP {src_ip} a scanné {len(port_scan_tracker[src_ip])} ports")
        port_scan_ip_src.append(src_ip)

def clear_list():
    now = int(time.time())
    if now - clear[0] > 20:
        ddos_ip_src.clear()
        brute_force_ip_src.clear()
        port_scan_ip_src.clear()

        # Données pour suivre l'activité réseau
        brute_force_tracker.clear()
        ddos_tracker.clear()
        port_scan_tracker.clear()
        clear[0] = now

def packet_handler(packet):
    """Traite les paquets capturés pour détecter des activités suspectes."""
    clear_list()
    if IP in packet:
        src_ip = packet[IP].src
        if TCP in packet:
            dst_port = packet[TCP].dport
            if packet[TCP].sport in ignore_src:
                return
            # Détection brute force
            detect_brute_force(packet)

            # Détection DDoS
            detect_ddos(src_ip)

            # Détection scan de ports
            detect_port_scan(src_ip, dst_port)

if __name__ == "__main__":
    print("[INFO] Détection en cours... Appuyez sur CTRL+C pour arrêter.")
    # Capture des paquets sur l'interface réseau
    
    sniff(iface="lo", prn=packet_handler, filter="tcp", store=0)
    
