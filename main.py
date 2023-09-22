import socket
import threading

def accept_client():
    while True:
        # Accepter la connexion
        cli_sock, cli_add = server.accept()
        CONNECTION_LIST.append(cli_sock)
        print('Connexion reçue de', cli_add)
        cli_sock.send(b'Merci de vous etre connecte')

        # Démarrer un thread pour gérer cette connexion
        thread_client = threading.Thread(target=broadcast_usr, args=(cli_sock,))
        thread_client.start()

def broadcast_usr(cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            if data:
                b_usr(cli_sock, data)
                print('Message reçu du client', data)
        except Exception as x:
            print(x)
            break

def b_usr(cs_sock, msg):
    for client in CONNECTION_LIST:
        if client != cs_sock:
            try:
                var_decode = 'Message venant de ' + client.getpeername()[0] + msg.decode('utf-8')

                client.send(var_decode.encode('utf-8'))
            except Exception as e:
                print(e)
                client.close()
                CONNECTION_LIST.remove(client)

if __name__ == "__main__":
    CONNECTION_LIST = []

    # Création du socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liaison du socket
    HOST = '10.4.1.209'
    PORT = 5051
    server.bind((HOST, PORT))

    # Écoute des clients
    server.listen(3)
    print('Serveur de chat démarré sur le port : ' + str(PORT))

    thread_ac = threading.Thread(target=accept_client)
    thread_ac.start()
