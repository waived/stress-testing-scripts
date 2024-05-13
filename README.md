This repository contains a small collection of transport layer Denial-of-Service scripts
that act effectively against Routers, Firewalls, Servers, and various IoT devices.

The descriptions are as follows...

ACK:
  The TCP-ACK (Acknowledge) flood is most effective against firewalls and servers, whereas
  routers and load balancers are often not susceptible to this attack. By taking advantage
  of vulnerabilities in the TCP three-way handshake, spoofed ACK packets are sent to the
  endpoint. The device will then attempt to make sense of these packets, trying to link them
  with a session that does not exist. In addition to causing general network congestion, 
  resource exhaustion is the true end goal of this attack. 

  This attack may be used in place of a standard SYN flood, as certain systems may make use
  of SYN-cookies, which thwart such an attack. Since ACK floods are not hindered by an SYN-
  cookie feature, they pass to the endpoint without being rejected.

ACK-FRAG:
  A Fragmented Acknowledge flood as a modified version of the standard TCP-ACK flood. In
  this specific example, the attack will generate a spoofed source address when sending the
  ACK packets. The attack will generate anywhere between 50 to 150 of these fragmented packets.
  The acknowledgement number of these ACK packets will stay the same, however the randomly
  generated initial sequence number will increase by one per each packet. Finally, a complete
  ACK packet will be send to the endpoint. The endpoint device will then struggle to piece
  together the ACK fragments, causing again, not only general network congestion, but
  resource exhaustion as well.

BOGUS:
  A bogus flood is an attack that sends packets to an endpoint with randomly chosen and enabled
  packet flags which act redundantly with each other. FIN-RST, SYN-FIN, URG-ECE-CWR, etc. The
  flags are randomly chosen per packet, containing a spoofed source address. The goal is to
  completely overwhelm the endpoint with as much incoherent requests as possible and bog the
  network down.

DOMINATE:
  This attack method is a variation of the well known SYN flood. Via a weakness in the TCP-
  3-way handshake, Dominate will initiate as many concurrent connections to the endpoint as
  possible. With the SYN flag set, Dominate also enables the ECE (Explicit Congestion Notification 
  Echo) and CWR (Content Window Reduced) flag as well.

  During a conversation between a client and a server, the client may send one or more requests.
  The server obviously serves the requests. However, when the server is under a heavy load
  (non-malicious network congestion) the server may choose the send response/s with the ECE
  flag enabled. This tells the client that the server network is experiencing congestion
  and that in order to maintain the integrity of their transveral, the client should
  reduce their content window size. If the client is ECN compliant, the client will have
  both the ECE and CWR flags enabled when sending any more packets. This also lets the server
  know that the requests have been downsized.

  In a dominate attack, these flags are already pre-set, letting the endpoint believe that
  the requests are being downsized. Variations of Dominate also contain junk data buffers.
  This type of attack can work effectively against some known load balancers and specifically
  has been known to take down prominent OVH services.

ESSYN:
  Explicit Spoofed SYN, or sometimes known as an XSYN flood. This flood is similar to the
  Dominate flood, and the basic of this flood mirrors an SYN flood. However, in addition
  to the SYN flag being set, the attack also sets the ECE flag, which signals congestion
  along the network path of the client. Although this flag truely servers no purpose, the
  goal is simply to add another layer of confusion, and this congestion control behavior 
  is designed only to further exhaust server-side resources at a fast rate. Since the
  source addresses are all spoofed, this bares no consequences at all for the attacker's
  network.

  Let it be known: this is a specific method based on the standard SYN flood, and because
  it was not created by network engineers, but by criminals, there has been some confusion
  as to what a true ESSYN/XSYN flood is. The most popular and inaccurate version of
  a 'ESSYN' flood is portrayed as a SYN/ACK flood.

L4:
  Short for 'Layer-4' flood, or sometimes known as a 'Layer-4 COMBO flood,' this attack
  is a conbination of both UDP and TCP floods. Here a dynamic data buffer is generated
  where the attacker specifies the range of bytes to generate per request, and the
  attacker spams the endpoint with these UDP/TCP packets containing an invalid data
  buffer. This attack is not spoofed and the attacker's true source address is exposed.

MIXABUSE:
  In this attack, the source address is spoofed to be the IP address belonging to the
  endpoint of the victim. From here, ICMP, UDP, and SYN (and SYN variations) are sent
  to another IP address by the victim's endpoint (although the packets are truly
  being sent by the attacker) These packets land at the network of the IP address.
  These requests appear not to be spoofed and the data buffers are static in both
  content and size. These packets are very identifiable and will be traced to the
  victim's endpoint instead of the attacker.

  The idea here is to send a Denial of Service attack on behalf of someone else.
  This attack will result in the IP address the traffic is being sent to blocking
  and/or reporting the IP of the victim endpoint. This attack is proven effective
  when encouranging one endpoint to block (blacklist) traffic from the victim.
  
  Example: a website that is selling sports merchandise is using a third-party 
  payment service (like PayIvy). The attacker uses MIXABUSE to attack PayIvy on
  behalf of the website. In turn, PayIvy defensively blocks all traffic coming 
  from the website's IP address, and therefore the website can no longer support
  payments, resulting in a loss of business when the legitimate users of the website
  try to purchase online merchandise. 

MIXAMP:
  This specific method is sometimes known as a 'UDP-MIX' flood. It is a reflective
  amplified Distributed Denial-of-Service attack. The attacker loads into the script a
  list of reflectors (servers who are running UDP service vulnerable to packet reflection
  attacks). The format for the list is <ip>:<port> and this method supports various
  services including but not limited to: DNS, NTP, CharGen, WS-Discovery, DVR IP Cameras,
  SSDP, SSMP, Microsoft SQL database, MemCache, etc.

  Here the source address of each packet is spoofed to be the victim's address. The 
  attacker spends specifically crafted packets to the IP:PORT found in the reflector
  list. These requests are then responsed to, and sent back to the victim's endpoint as
  the services believe they are the one who made the request. Because these mixed service
  types are 'amplified' (or sent more data to the victim than what was requested) the
  attack has a larger data overhead and puts more or a strain on the victim's network.

RST: 
  Sometimes known as a 'TCP-Reset' flood, this attack sends RST packets to the
  endpoint. An RST packet essentially asks the endpoint to re-initiate the
  connection and start over. Here the connection will hang and eat up server-
  side resources. Eventually, the endpoint will being to drop legitimate connections
  and become inaccessible to legitimate users. Each packet contains a spoofed
  source address.

SSYN:
  As per some of the other methods covered, this is a Spoofed SYN (Synchronize) flood. Here the
  attacker sends as many SYN packets with a spoofed source address. This results in the endpoint
  to send a SYN-ACK (Synchronize-Acknowledge) packet to the spoofed IP address and await the
  final ACK packet. It never comes, and the attack will generate/send as many SYN requests as possible.
  This ultimately will result in the endpoint reserving and finally exhausting all available TCP sockets
  to give out. Any other legitimate traffic will be at a loss. Once a connection is disposed of, the
  TCP socket will go into a TIME_WAIT status, where it will remained reserved for up to 60sec before
  being available again. This is to ensure no lingering traffic comes through. Once another available
  connection opens up, the attack will once again consume the connection availability.

  Note: this attack will be rendered useless is the endpoint has SYN-cookies enabled. To bypass
  this security measure, use other attacks instead, such as ACK, ACKFRAG, RST, etc. 

SYNACK:
  This attack leverages the TCP 3-way handshake vulnerability by starting off the conversation in the
  middle. Instead of sending a SYN packet to initiate a TCP connection, it sends a SYN+ACK packet to
  the endpoint. The endpoint then assume a handshake was already made, originating from the device or
  network and attempt to send a final ACK packet unfruitfully to spoofed source address. The end goal
  is to consume all server-side resources.

TSUNAMI:
  This attack is also known as a PSH+ACK (Push Acknowledge) flood. The PSH flag instructs the endpoint
  to process the data immediately, raising its priority level, and the ACK flag denotes the end of the
  TCP 3-way handshake. However, in this attack the PSH+ACK packet also contains a junk data buffer. This
  buffer is dynamic in size and content, specified by the attacker, and makes a hybrid DoS attack out of
  both volumetric and protocol abuse methods. It also manages to bypass SYN-cookies entirely. It puts
  load on the endpoint network and additionally creates server-side confusion.

SUDP:
  Spoofed UDP (datagram flood) takes advantage of weaknesses in the UDP protocol. Since this is a connectionless
  protocol, the source address can easily be spoofed. This attack incorperates a dynamic data buffer in both
  size and content, specified by the user. Its volumetric capabilities overwhelm the endpoint network and leave
  server-side resources exhausted.

XMAS:
  This is known as a Christmas flood, since all the packet flags are 'lit up' like a Christmas tree. Each
  packet, which contains a spoofed source address, sends all of the packet flags at once: SYN, ACK, URG, PSH,
  FIN, ECE, CWR, and RST. This attack overwhelms the target system, consuming its resources and causing it to
  become unresponsive to legitimate traffic. This attack is also known as a 'TCP All-flag' attack.
