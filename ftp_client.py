import ftplib,os

def getfile(ftp,filename):
    try:
        ftp.retrbinary("RETR " + filename, open(filename,"wb").write)
        print("Download complete")
    except Exception as err:
        print("Error downloading file" + filename  + str(err))

def upload(ftp ,filename):
    ext = os.path.splitext(filename)[1]
    try:
        if ext in (".txt",".html",".htm",".csv"):
            ftp.storlines("STOR " + filename,open(filename))
        else:
            ftp.storbinary("STOR " + filename,open(filename,"rb"),1024)
        print("upload complete")
    except Exception as err:
        print("Upload Failed" + str(err))

ftp = ftplib.FTP("ftp.nluug.nl")
ftp.login("anonymous","ftplib-example")

data = []

ftp.cwd("/pub")
ftp.dir(data.append)
for i in data:
    print("-" + i)

print("Downloading README...")
getfile(ftp, "README.nluug")

#cant upload in this server as we dont have permission in public repositories
print("Uploading...")
upload(ftp,"README.nluug")

ftp.quit()