import socket

target_host = "127.0.0.1"
target_port = 80

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect((target_host, target_port))

# Send some data
client.send(b"Hello Server!")

# Receive the response
response = client.recv(4096)
print(response.decode('utf-8'))

client.close()
