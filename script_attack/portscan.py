from pwn import *


def portscan_attack(ip, start_port, end_port):
    for port in range(start_port, end_port):
        try:
            target = remote(ip, port)
            print(f"Port {port} is open.")
            target.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            #print(target.recvuntil(b"Simulated vulnerable server").decode())
            target.close()
        except Exception as e:
            print(f"Port {port} is closed or unreacheble. Error: {e}")

if __name__ == "__main__":
    ip = "localhost"
    start_port = 70
    end_port = 100
    portscan_attack(ip, start_port, end_port)    
