import os, argparse, socket ,socketserver ,binascii


class tcpServer(socketserver, BaseRequestHandler):
	def handle(self):
		data = self.request.recv(512).strip()
		if data.startswith(b"send: "):
			filename = data.split(b":")[1]
			print("[Receiving file] " + file.decode())
			with open(str(file.decode("utf-8")),"wb") as f:
				data = bytearray(self.request.recv(512).strip())
				if len(data) % 2 == 0:
					f.write(binascii.unhexlify(data))
				else:
					f.write(binascii.unhexlify(data.append(0)))
		print("_________[File Received]_________")


def startServer(args):
	server = scoketserver.TCPServer(("127.0.0.1",args.port),tcpServer)
	print("[Server Started]")
	server.serve_forever()

def startClient(args):
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((args.ip,args.port))
	path, filename = os.path.split(args.file)
	print("[Sending file] " + args.file)
	client.sendall(b"send: " + bytes(filename, "utf-8"))
	with open(args.file, "rb") as f:
		data = f.read(512)
		while (data):
			client.sendall(binascii.hexlify(data))
			data = f.read(512)
	client.close()
	print("[File Sent] " + args.file)

def main(args):
	if (args.client):
		startClient(args)
	elif (args.server):
		startServer(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", action="store", help="start client", type=str, nargs="?", default=False,const=True)
    parser.add_argument("-s", "--server", action="store", help="start server", type=str, nargs="?", default=False,const=True)
    parser.add_argument("-i", "--ip",     action="store", help="remote server ip", type=str)
    parser.add_argument("-p", "--port",   action="store", help="remote server ip", type=int)
    parser.add_argument("-f", "--file",   action="store", help="remote server ip", type=str)
    args = parser.parse_args()

    if (not args.client and not args.server):
            parser.print_help()
            print("\n You must specify --client or --server")
            parser.exit()
    main(args)
