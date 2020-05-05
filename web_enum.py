import requests, sys, multiprocessing, time, argparse
from datetime import datetime

#url is just the ip (in argparse)

def request(url):
    try:
        agent = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"
        }
        rsp = requests.get(url)
        if rsp.status_code != 404:
            print("[+] status " + str(rsp.status_code) + ": " + url)
    except Exception as err:
        print("[-] Error while Requesting " + str(err))

def scan(url, word, ext):
    temp_url = "http://" + url + word.rstrip()
    request(temp_url)
    if ext:
        request(temp_url + ext)

def main(args):
    starttime = datetime.now()
    print("_____________________________________________________________")
    print("Started @ " + str(starttime))
    print("_____________________________________________________________")

    if args.url.endswith("/") == False:
        args.url += "/"
    with open(args.wordlist) as f:
        for word in f:
            if word.startswith("#") == False:
                p = multiprocessing.Process(target = scan, args=(args.url, word, args.extension))
                p.start()
    
    stoptime = datetime.now()
    print("_____________________________________________________________")
    print("Scan Duration: " + str(stoptime - starttime))
    print("Completed @ " + str(stoptime))
    print("_____________________________________________________________")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url" ,action="store", help = "starting url")
    parser.add_argument("wordlist" ,action="store", help = "list of paths/files")
    parser.add_argument("-e", "--extension" ,action="store", help = "file extension")
 
    if len(sys.argv[2:]) == 0:
        parser.print_help()
        parser.exit()
    
    args = parser.parse_args()
    main(args)