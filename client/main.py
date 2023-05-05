import socket
import json

host = "localhost"
port = 1234

# connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# send a message to the server
json_info = {"username" : "worldxdana", "password": "123qwe123"}
message = "Hello, server!"
client_socket.send(json.dumps(json_info).encode())

# receive a response from the server
response = client_socket.recv(1024).decode()
print(f"Received response from server: {response}")

# close the connection
client_socket.close()
