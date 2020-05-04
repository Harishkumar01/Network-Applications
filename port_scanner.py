import argparse, sys, multiprocessing, logging
from scapy.all import *
from datetime import datetime
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0


def scanPort(ip, port):
    srcp = RandShort()
    pkt = sr1(IP(dst=ip) / TCP(sport = srcp, dport = port, flags = "S"))

    if pkt is not None:
        flag = pkt.getlayer(TCP).flags
        if flag == 0x12: #syn, ack
            print("[+] Port: " + str(port) + " open")
            send(IP(dst = ip) / TCP(sport = srcp, dport = port, flags = "R"))
        else:
            print("[-] Port: " + str(port) + " closed")
    else:
        print("[-] Device Unreachable ")

        

def main(args):
    try:
        starttime = datetime.now()
        args.throttle = float(args.throttle)
        print("_____________________________________________________________")
        print("[+] Scanning ports of " + args.IP + " from port " + "[" + str(args.sport) + "] to [" + str(args.eport) + "]")
        print("Started @ " + str(starttime))
        print("_____________________________________________________________")

        for port in range(int(args.sport), int(args.eport)+1):
            #p = multiprocessing.Process(target=scanPort,args=(args.IP, port))
            #p.start()
            scanPort(args.IP, port)
            #time.sleep(args.throttle)
        time.sleep(2)
        stoptime = datetime.now()

        print("_____________________________________________________________")
        print("Scan Duration: " + str(stoptime - starttime))
        print("Completed @ " + str(stoptime))
        print("_____________________________________________________________")


    except Exception as err:
        print("[-] Error while Scanning " + str(err))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP" ,action="store", help = "ip address of the device to be scanned", type=str)
    parser.add_argument("sport" ,action="store", nargs="?", default=1, const=1, help = "Start Port Range", type=int)
    parser.add_argument("eport" ,action="store", nargs="?", default=1023, const=1023, help = "End Port Range", type=int)
    parser.add_argument("-t", "--throttle" ,action="store", nargs="?", default=0.25, const=0.25, help = "Throttle connection Attempts")

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    
    args = parser.parse_args()
    main(args)