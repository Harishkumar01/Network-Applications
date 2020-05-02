# install cruptography==2.9.2 latest version

import paramiko

hostname = "127.0.0.1"
username = "harish-kumar"
passwd = "vharishkj"
port = 1337

srcdown = "/home/harish-kumar/sftp_down.txt"
srcup = "/home/harish-kumar/Network-Applications/sftp_up.txt"
desdown = "/home/harish-kumar/Network-Applications/sftp_down.txt"
desup = "/home/harish-kumar/sftp_up.txt"

try:
	p = paramiko.Transport((hostname,port))
	p.connect(username=username,password=passwd)
	print("Connected to " + hostname + " via SSH")
	sftp = paramiko.SFTPClient.from_transport(p)
	print("Starting Download")
	sftp.get(srcdown,desdown)
	print("Download Complete")
	print("Starting File upload")
	sftp.put(srcup,desup)
	print("Upload Complete")
	p.close()
	print("Disconnected from the server")

except Exceptions as err:
	print("Error in Sftp transmission " + str(err))

