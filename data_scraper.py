import re, requests, sys, argparse

class RegEx:
    def __init__(self, pattern, desc):
        self.pattern = pattern
        self.desc = desc

#rgxEmail = RegEx(r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
rgxEmail = RegEx(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+","Emails")
rgxPhone = RegEx(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "Phone Numbers")
rgxIP = RegEx(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b","IP Addresses")
rgxWords = RegEx(r"[a-zA-Z]+","Words")

def scrapeURL(url, rgx):
    try:
        src = requests.get(url.strip())
        for rg in rgx:
            print("[+] Scrapping " + rg.desc + "from " + url.strip())
            res = set(re.findall(rg.pattern, src.text, re.I))
            for data in res:
                print(data)

    except Exception as err:
        print("Error Scraping URL " + str(err))

def scrapeFile(filename, rgx):
    try:
        with open(filename) as fh:
            for url in fh:
                scrapeURL(url, rgx)

    except Exception as err:
        print("Error Scraping File " + str(err))

def main(args):
    rgx = []
    isFile = True
    if args.input.lower().startswith("http"):
        isFile = False
    if args.scrape.lower() == "e": #scrape emails
        rgx = [rgxEmail]
    elif args.scrape.lower() == "p": #scrape phone numbers
        rgx = [rgxPhone]
    elif args.scrape.lower() == "w": #scrape words
        rgx = [rgxWords]
    elif args.scrape.lower() == "i": #scrape ip
        rgx = [rgxIP]
    elif args.scrape.lower() == "a": #scrape everything
        rgx = [rgxEmail, rgxPhone, rgxWords, rgxIP]

    if (isFile):
        scrapeFile(args.input, rgx)
    else:
        scrapeURL(args.input, rgx)

    print("____________________________________________________")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", action="store", help="The URL or file containing URLs", type=str)
    parser.add_argument("scrape", action="store", help="e: email, p: phone, i: ips, w: Words, a: All ", type=str, nargs="?", default="a")

    if len(sys.argv[2:])== 0:
        parser.print_help()
        parser.exit()
    
    args = parser.parse_args()
    main(args)

