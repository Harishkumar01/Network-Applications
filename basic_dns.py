import socket

try:
    print("Domain name for the given ip : " + socket.getfqdn("8.8.8.8"))
    print("Domain name to ip : " + socket.gethostbyname("beyondthepavilion.site"))
    print("Domain name to ip : " + str(socket.gethostbyname_ex("beyondthepavilion.site")))
    print("Domain name of localmachine : " + socket.gethostname())
except Exception as err:
    print("Error : " + str(err))