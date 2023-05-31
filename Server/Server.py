import socket
from DBhandler import DBHandler
import json
import socket
import threading
from Password import Password

#server class is supposed to activate a server
#to preform user action
class Server:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.DBhandler = DBHandler(db_name)
        self.server_socket = None
        self.loggedClients = []

    #start function to make server work.
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Received connection from {client_address}")
            #opening a new thread to handle client request.
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            thread.start()

    #function to handle client requests (at this point login).
    def handle_client(self, client_socket, client_address):
        try:
            while True:
                # receive data from the client
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                json_info = handle_info(data)    
                response = self.action_handler(json_info)                        
                client_socket.send(response.encode())

        #in case something goes wrong, we should handle the error.
        except Exception as e:
            print(f"Exception while handling client {client_address}: {e}")
        finally:
            # close the connection
            print(f"Closing connection with {client_address}")
            client_socket.close()

    def action_handler(self, json_info):
        if(json_info["Action"] == "login"):
            return self.login_handler(json_info)              

        if(json_info["Action"] == "register"):
            return self.register_handler(json_info)
        
        if(json_info["Action"] == "logout"):
            return self.logout_handler(json_info)
        
        if(json_info["Action"] == "insert"):
            return self.newPass_handler(json_info)
        
        if(json_info["Action"] == "getAllPasses"):
            return self.UserView_handler(json_info)

    def UserView_handler(self, json_info):
        try:
            passwords = self.DBhandler.getAllUserPassword(json_info["Username"])
        except Exception as e:
            passwords = f"password retrival failed"
        finally:
            json_info = json.dumps(passwords)
            return json_info
         
    def newPass_handler(self, json_info):
        print("in newpass")
        try:
            password = Password(json_info["Url"], json_info["Password"], json_info["Owner"])
            if(self.DBhandler.insert_password(json_info)):
                response = f"password inserted succesfully"
            else:    
                response = f"you already entered this password"
            
        except Exception as e:
            response = f"ERRROR WHILE LOGGING OUT:" + e
            print(response)
        finally:
            return response
        
        
    def logout_handler(self, json_info):
        #add mutex support if agreed
        try:
            self.loggedClients.remove(json_info["Username"])
            response = f"user " + json_info["Username"] + " has logged out"
            print(response)
        except Exception as e:
            response = f"ERRROR WHILE LOGGING OUT:" + e
            print(response)
        finally:
            return response

    def register_handler(self, json_info):
        if(self.DBhandler.signup(json_info["Username"], json_info["Password"])):
            response = f"signup was completed, you may now log into thew system."
        else:
            response = f"sign-up didn't work."
        return response
           
    
    def login_handler(self, json_info):
        if(self.DBhandler.login(json_info["Username"], json_info["Password"] )):
            self.loggedClients.append(json_info["Username"])
            response = f"Hello, I received your message!"
        else:
            response = f"sorry, you're not signed yet."
        return response

#a function to make the json a dictionary.
#of information
def handle_info(data):
    data_dict = json.loads(data)   
    #print(type(data_dict))
    #print(data_dict["username"])
    return data_dict