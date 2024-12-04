from pwn import *


def portscan_attack(ip, start_port, end_port):
    with open("attack_log", "+a") as f:
        f.write(f"Port Scan Results for {ip} (Ports Range {start_port} -- {end_port}):\n")
        for port in range(start_port, end_port):
            try:
                target = remote(ip, port)
                f.write(f"Port {port} is open.\n")
                target.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                target.close()
            except Exception as e:
                continue

if __name__ == "__main__":
    ip = "localhost"
    start_port = 70
    end_port = 400
    portscan_attack(ip, start_port, end_port)    
