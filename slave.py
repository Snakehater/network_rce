import socket
from multicast_dns import *

def client_program():
    ip = listen_dns()

    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((ip, port))  # connect to the server

    while True:
        data = client_socket.recv(1024).decode()
        if data == "stop":
            break
        print(data)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
