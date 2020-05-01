#install popa3d //sudo apt install popa3d
#mail -s //to ur local machine
#sudo service popa3d start


import poplib
from email.message import EmailMessage

server = "127.0.0.1"
user = "harish-kumar"
passwd = "" 
#passwd of linux

server = poplib.POP3(server)
server.user(user)
server.pass_(passwd)

msgcount = len(server.list()[1])

for i in range(msgcount):
	for msg in server.retr(i+1)[1]:
		print(msg.decode())

