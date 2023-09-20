import socket, threading
import time


def accept_client():
    while True:
        #accept
        cli_sock, cli_add = server.accept()
        CONNECTION_LIST.append(cli_sock)
        print('Got connection from', cli_add)
        cli_sock.send(b'Thank you for your connecting')
        cli_sock.close()

        thread_client = threading.Thread(target = broadcast_usr, args=[cli_sock])
        thread_client.start()

def broadcast_usr(cli_sock):
    while True:
        try:
            data = cli_sock.recv(2024)
            if data:
               b_usr(cli_sock, data)
               print('message received from client', data)
        except Exception as x:
            print(x.message)
            break

def b_usr(cs_sock, msg):
    for client in CONNECTION_LIST:
        if client != cs_sock:
            client.send(msg)
            print('Got connection from', msg)

if __name__ == "__main__":
    CONNECTION_LIST = []

    # socket creation
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind socket
    HOST = '10.4.1.209'
    PORT = 5051
    server.bind((HOST, PORT))

    # listen client
    server.listen(3)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target = accept_client)
    thread_ac.start()
