__author__ = 'rcj1492'
__created__ = '2015.07'


# https://stackoverflow.com/questions/1117958/how-do-i-use-raw-socket-in-python
# https://docs.python.org/2/library/socket.html

# import socket
# http://hackoftheday.securitytube.net/2013/03/wi-fi-sniffer-in-10-lines-of-python.html

def sniffNet():
    rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    rawSocket.bind(("mon0", 0x0003))
    ap_list = set()
    while True:
        pkt = raw.recvfrom(2048)[0]
        if pkt[26] == "\x80":
            if pkt[36:42] not in ap_list and ord(pkt[63]) > 0:
                ap_list.add(pkt[36:42])
                print("SSID: %s  AP MAC: %s" % (pkt[64:64 +ord(pkt[63])], pkt[36:42].encode('hex')))
# sniffNet()

# pip install scapy-python3
# from scapy.all import *
def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subType == 8:
            if pkt.addr2 not in ap_list:
                ap_list.append(pkt.addr2)
                print("AP MAC: %s with SSID: %s" %(pkt.addr2, pkt.info))
# ap_list = []
# sniff(iface='mon0', prn=PacketHandler)

# https://docs.python.org/2/library/socket.html
# requires administrator privileges to modify the interface:
def sniffNetworks():

    # the public network interface
    HOST = socket.gethostbyname(socket.gethostname())

    # create a raw socket and bind it to the public interface
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((HOST, 0))

    # Include IP headers
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packages
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # receive a package
    print(s.recvfrom(65565))

    # disabled promiscuous mode
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
# sniffNetworks()
