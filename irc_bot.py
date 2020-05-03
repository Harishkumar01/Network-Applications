import socket

class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def send(self, channel, msg):
        self.irc.send(("PRIVMSG " + channel + " : " + msg + "\n").encode())

    def connect(self, server, channel, botname):
        print("COnnecting to server: " + server)
        self.irc.connect((server,6667))
        self.irc.send(("USER " + botname + " " + botname + " " + botname + " : This is a fun bot\n").encode())
        self.irc.send(("NICK " + botname + "\n").encode())
        self.irc.send(("JOIN " + channel + "\n").encode())

    def get_text(self):
        text = self.irc.recv(2040)
        return text

channel = "#testchan123"
server = "irc.freenode.com"
nickname = "botbotty01"

irc = IRC()
irc.connect(server,channel,nickname)

while True:
    text = irc.get_text()
    print(text.decode())
    if b"PRIVMSG" in text and channel.encode() in text and b":hello" in text:
        user = text.strip().split(b"~")[0][1:-1].decode()
        irc.send(channel, "Hello " + user + " !\n")