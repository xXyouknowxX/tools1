#THIS IS SERVER AND CLIENT
#How to use:
#To start the server: python ncat.py server 0.0.0.0 9999
#To start the client: python ncat.py client 127.0.0.1 9999

import sys
import socket
import subprocess
import threading

def execute_command(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

def handle_client(client_socket):
    while True:
        cmd_buffer = client_socket.recv(1024).decode('utf-8').strip()
        if not cmd_buffer:
            break
        response = execute_command(cmd_buffer)
        client_socket.send(response)
    client_socket.close()

def server_loop(bind_ip, bind_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print(f"[*] Listening on {bind_ip}:{bind_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def client_sender(target_host, target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    while True:
        cmd = input("<nc-shell>")
        if cmd == "exit":
            break
        client.send(cmd.encode('utf-8'))
        response = client.recv(4096)
        print(response.decode('utf-8'), end="")

    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: netcat_tool.py {server|client} target_host target_port")
        sys.exit(0)
    
    mode = sys.argv[1]
    target_host = sys.argv[2]
    target_port = int(sys.argv[3])

    if mode == "server":
        server_loop(target_host, target_port)
    elif mode == "client":
        client_sender(target_host, target_port)
    else:
        print("Invalid mode specified.")
        sys.exit(0)
