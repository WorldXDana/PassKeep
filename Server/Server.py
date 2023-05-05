import socket
from DBhandler import DBHandler
import json
import socket
import threading

class Server:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.DBhandler = DBHandler(db_name)
        self.server_socket = None


    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Received connection from {client_address}")
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            thread.start()

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                # receive data from the client
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                #print(f"Received data from {client_address}: {data}")

                # send a response back to the client
                json_info = handle_info(data)   
                #print(json_info["username"])
                if(self.DBhandler.login(json_info["username"], json_info["password"] )):
                    response = f"Hello, {client_address[0]}! I received your message: {data}"
                else:
                    response = f"sorry, you're not signed yet."
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Exception while handling client {client_address}: {e}")
        finally:
            # close the connection
            print(f"Closing connection with {client_address}")
            client_socket.close()

def handle_info(data):
    data_dict = json.loads(data)   
    print(type(data_dict))
    print(data_dict["username"])
    return data_dict