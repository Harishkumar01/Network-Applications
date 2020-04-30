import urllib.request

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0" 

req = urllib.request.Request("http://beyondthepavilion.site",headers=headers)
html = urllib.request.urlopen(req).read()
print(html.decode())

print("Downloading wordpress file for example....")
rsp = urllib.request.urlopen("http://wordpress.org/latest.zip")
data = rsp.read()

filename = "wordpress.zip"
file_ = open(filename,"wb")
file_.write(data)
file_.close()
print("Dowloaded file")