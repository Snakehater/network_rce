import socket
import _thread
from multicast_dns import *
import json

clients_file = "clients.json"
clients_json = {}
clients = []

def save_json():
    global clients_json
    with open(clients_file, "w") as of:
        of.write(json.dumps(clients_json, indent=4))

def open_json():
    global clients_json
    with open(clients_file, "r") as infi:
        clients_json = json.load(infi)

class Client:
    name = None
    ip_port = None
    cs = None
    def __init__(self, client_socket, ip_address_port):
        self.cs = client_socket
        self.ip_port = ip_address_port

def client_thread(cs, addr):
    while True:
        msg = cs.recv(1024).decode('iso-8859-1')
        if msg == "exit" or msg == "":
            break
        print(addr, ":")
        print(msg.replace("\\n", '\n'))
    cs.close()
    for i in range(len(clients)):
        if (addr[0] == clients[i].ip_port[0]):
            clients.pop(i)

def accept_clients(s, hostname, host_ip):
    while True:
        cs, addr = s.accept()
        _thread.start_new_thread(client_thread, (cs, addr))
        clients.append(Client(cs, addr))
        open_json()
        try:
            clients[len(clients) - 1].name = clients_json[addr[0]]
        except:
            pass

selected_client = -1

def server_program():
    global selected_client
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    open_json()

    # get the hostname
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    port = 5000  # initiate port no above 1024

    advertise_dns(socket.gethostbyname(host))

    s.bind((ip, port))

    s.listen(5)
    _thread.start_new_thread(accept_clients, (s, host, ip))

    while True:
        r = input("> ")
        match r:
            case "q":
                break
            case "list":
                if len(clients) == 0:
                    print("No clients are connected")
                for client in clients:
                    print(client.ip_port, " -> ", client.name)
            case "ping":
                advertise_dns(socket.gethostbyname(host))

        if r.startswith("name"):
            if len(r.split(" ")) != 3:
                print("Invalid command, expected: name <ip> <new_name>")

            for i in range(len(clients)):
                if clients[i].ip_port[0] == r.split(" ")[1]:
                    clients[i].name = r.split(" ")[2]
                    clients_json[clients[i].ip_port[0]] = clients[i].name
                    save_json()

        if r.startswith("select"):
            for i in range(len(clients)):
                if clients[i].name == r.split(" ")[1]:
                    selected_client = i
                    break

        if r.startswith("r "):
            if selected_client < 0:
                print("No client selected, select with 'name <ip> <new_name>'")
            else:
                clients[selected_client].cs.send(bytes(r[2:], "utf-8"))

    save_json()
    s.close()  # close the connection


if __name__ == '__main__':
    server_program()
