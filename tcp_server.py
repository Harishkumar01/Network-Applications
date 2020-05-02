import socket

hostname = "127.0.0.1"
port = 8081

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
    server.bind((hostname,port))
    server.listen()
    conn,addr = server.accept()

    with conn:
        print("Client Connected " + str(addr))
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

