import socket
import _thread

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
    port = 5000  # initiate port no above 1024

    s.bind((host, port))

    s.listen(5)
    while True:
        cs, addr = s.accept()
        _thread.start_new_thread(client_thread, (cs, addr))

    s.close()  # close the connection


if __name__ == '__main__':
    server_program()
