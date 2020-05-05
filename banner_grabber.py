import sys, argparse, socket, multiprocessing, subprocess, time
from datetime import datetime

def scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        res = s.connect_ex((ip,port))
        if res == 0:
            if port == 80: #http
                rsp = "HEAD / HTTP/1.1\r\nhost: " + ip + "\r\n\r\n"
                s.send(rsp.encode())
            banner = s.recv(4096)
            msg = "[+] Port " + str(port) + " open\n"
            msg += "--------------------------------------\n" + banner.strip().decode()
            print(msg + "\n------------------------------------------------\n")
        s.close()
    except socket.timeout:
        banner = "NO banner Message"
        if port == 53: #dns 
            banner = subprocess.getoutput("nslookup -type=any -class=chaos version.bind " + ip)
        msg = "[+] Port " + str(port) + " open\n"
        msg += "--------------------------------------\n" + banner.strip().decode()
        print(msg + "\n------------------------------------------------\n")
        s.close()
    
def main(args):
    try:
        args.throttle = float(args.throttle)
        starttime = datetime.now()
        print("_____________________________________________________________")
        print("[+] Scanning ports of " + args.IP + " from port " + "[" + str(args.sport) + "] to [" + str(args.eport) + "]")
        print("Started @ " + str(starttime))
        print("_____________________________________________________________")

        for port in range(int(args.sport), int(args.eport)+1):
            p = multiprocessing.Process(target=scan,args=(args.IP, port))
            p.start()
            #scan(args.IP, port)
            time.sleep(args.throttle)
        time.sleep(3)
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
    parser.add_argument("sport" ,action="store", nargs="?", default=1, help = "Start Port Range", type=int)
    parser.add_argument("eport" ,action="store", nargs="?", default=1024, help = "End Port Range", type=int)
    parser.add_argument("-t", "--throttle" ,action="store", nargs="?", default=0.25, const=0.05, help = "Throttle connection Attempts")
 
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    
    args = parser.parse_args()
    main(args)