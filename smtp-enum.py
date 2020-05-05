import socket, sys, argparse
from datetime import datetime

def scan(ip, users):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip, 25))
        rsp = s.recv(1024)
        s.send(b"HELO Friend\n")
        rsp = s.recv(1024)

        if b"250" not in rsp:
            print("[!] Something went wrong, exiting.")
            sys.exit(0)

        s.send(b"MAIL FROM:hi@me.com\n")
        rsp = s.recv(1024)
        if b"250" not in rsp:
            print("[!] Something went wrong, exiting....")
            sys.exit(0)
        
        for user in users:
            s.send(b"RCPT TO:" + user.rstrip().encode() + b"\n")
            rsp = s.recv(1024)
            if b"250" not in rsp:
                print("[+] Valid: " + user.rstrip())

        s.send(b"QUIT\n")
        s.close()

    except Exception as err:
        print("[-] Error While Scanning " + str(err))

def main(args):
    starttime = datetime.now()
    print("_____________________________________________________________")
    print("Started @ " + str(starttime))
    print("_____________________________________________________________")

    with open(args.wordlist) as f:
        usr = []
        if args.batch != 0:
            for user in f:
                if(len(usr) + 1) != args.batch:
                    usr.append(user)
                else:
                    usr.append(user)
                    scan(args.ip, usr)
                    del usr[:]
            if len(usr) > 0:
                scan(args.ip, usr)
        else: #NO batches
            scan(args.ip, f)
    
    stoptime = datetime.now()
    print("_____________________________________________________________")
    print("Scan Duration: " + str(stoptime - starttime))
    print("Completed @ " + str(stoptime))
    print("_____________________________________________________________")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP" ,action="store", help = "ip address of the remote smtp server")
    parser.add_argument("wordlist" ,action="store", help = "wordlist of usernames")
    parser.add_argument("-b", "--batch" ,action="store", nargs="?", default=0, const=10, help = "Attempts per connection", type=int)
 
    if len(sys.argv[2:]) == 0:
        parser.print_help()
        parser.exit()
    
    args = parser.parse_args()
    main(args)