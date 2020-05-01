import paramiko

hostname = "127.0.0.1"
port = 1337 #change port accordingly
user = "harish-kumar"
#enter local password(ubuntu)
passwd = ""

try:
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname, port = port, username = user, password = passwd)

	while True:
		try:
			cmd = input("$> ")
			if cmd == "exit": break
			stdin,stdout,stderr = client.exec_command(cmd)
			print(stdout.read().decode())
		except KeyboardInterrupt:
			break
except Exception as err:
	print("Error while logging: " + str(err))
