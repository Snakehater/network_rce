import socket
import _thread
from multicast_dns import *

def client_thread(cs, addr):
    while True:
        msg = cs.recv(1024)
        print(msg)
        if msg == bytes("exit", "utf-8"):
            break
        print(addr, " >> ", msg)
        cs.send(bytes("ACK", "utf-8"))
    cs.close()

def server_program():
    s = socket.socket()

    # get the hostname
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    port = 5000  # initiate port no above 1024

    advertise_dns(socket.gethostbyname(host))

    s.bind((ip, port))

    s.listen(5)
    while True:
        cs, addr = s.accept()
        _thread.start_new_thread(client_thread, (cs, addr))

    s.close()  # close the connection


if __name__ == '__main__':
    server_program()
