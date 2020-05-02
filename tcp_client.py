import socket

hostname = "127.0.0.1"
port = 8081

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
    client.connect((hostname, port))
    client.sendall(b"hi harish here")
    data = client.recv(1024)

print("Message echoed from server " + repr(data.decode()))
