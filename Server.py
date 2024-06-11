import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)
print ("[*] Server started on: %s%d" % (bind_ip,bind_port))

#handel connections
def handel_connection(client_socket):
    request = client_socket.recv(1024)
    print ("[*]Recived: %s" % request.decode('utf-8'))
    client_socket.send(b"ACK!")
    client_socket.close
while True:
    client, addr = server.accept()
    print("[*]Accepted connection from: %s:%d" % (addr[0], addr[1]))

    client_handler = threading.Thread(target=handel_connection, args=(client,))
    client_handler.start()