# Network traffic is a concern (witnessed in arpScan)
# Implement threading in ip,tcp scan to improve efficiency

import multiprocessing, sys, netaddr, argparse, logging
from scapy.all import *
from datetime import datetime
logging.getLogger("scapy.runetime").setLevel(logging.ERROR)
conf.verb = 0

class const:
    ARP = 0
    PING = 1  
    TCP = 2

def arpScan(subnet):
    ans,unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst = subnet), timeout = 2)
    for snd,rcv in ans:
        print(rcv.sprintf(r"[+] [ARP] Online: %ARP.psrc% - %Ether.src%"))

def ping(ip):
    reply = sr1(IP(dst=str(ip)) / ICMP(), timeout=3)
    if reply is not None:
        print("[+] [PING] Online: " + str(ip))
    else:
        print("[+] [OFFLINE]: " + str(ip))

def tcp(ip):
    port = 53
    srcp = RandShort()
    pkt = sr1(IP(dst=str(ip)) / TCP(sport = srcp, dport = port, flags = "S"), timeout=5)

    if pkt is not None:
        flag = pkt.getlayer(TCP).flags
        if flag == 0x12: #syn, ack
            print("[+] [TCP] Online: " + str(ip) + "- replied with syn,ack")
            send(IP(dst = str(ip)) / TCP(sport = srcp, dport = port, flags = "R"))
        elif flag == 0x14: #Reset but host still alive
            print("[+] [TCP] Online: " + str(ip) + "- replied with reset(RST),ack")
        else:
            print("[+] [TCP] Online: " + str(ip))
    else:
        print("[+] [OFFLINE]: " + str(ip))

def scan(subnet, typeval):
#    jobs = []
#    for ip in subnet:
#        if typeval == const.PING:
#            p = multiprocessing.Process(target=ping, args=(ip,))
#            jobs.append(p)
#            p.start()
#        else:
#            p = multiprocessing.Process(target=tcp, args=(ip,))
#            jobs.append(p)
#            p.start()
#
#    for j in jobs:
#        j.join()
    if typeval == const.PING:
        for ip in subnet:
            ping(ip)
    if typeval == const.TCP:
        for ip in subnet:
            tcp(ip)

def main(args):
    try:
        subnet = netaddr.IPNetwork(args.subnet)
        starttime = datetime.now()
        print("___________________________________________________________________")
        print("[+] Scanning from " + str(subnet[0]) + " to " + str(subnet[-1]))
        print("[+] Started @ " + str(starttime))
        print("___________________________________________________________________")

        if args.scantype == const.ARP:
            arpScan(args.subnet)
        elif args.scantype == const.PING:
            scan(subnet, const.PING)
        elif args.scantype == const.TCP:
            scan(subnet, const.TCP)
        else:
            arpScan(args.subnet)
            scan(subnet, const.PING)
            scan(subnet, const.TCP)

        stoptime = datetime.now()
        print("___________________________________________________________________")
        print("[+] Scan Duration " + str(stoptime - starttime))
        print("[+] Completed @ " + str(stoptime))
        print("___________________________________________________________________")


    except Exception as err:
        print("[-] Error while scanning " + str(err))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subnet", action="store", help="subnet to scan for hosts", type=str)
    parser.add_argument("scantype", action="store", nargs="?", default=3, help="Type of scan: [0 = ARP, 1 = PING(icmp), 2 = TCP, 3 = ALL] ", type=int)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(args)

