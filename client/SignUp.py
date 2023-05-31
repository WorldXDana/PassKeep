import tkinter as tk
import socket
import json

class SignUp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack() 
        self.create_widgets()
    
    def create_widgets(self):
        self.username_label = tk.Label(self)
        self.username_label["text"] = "Username:"
        self.username_label.pack()

        # create an entry field for the username
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.email_label = tk.Label(self)
        self.email_label["text"] = "email:"
        self.email_label.pack()

        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        # create a label for the password field
        self.password_label = tk.Label(self)
        self.password_label["text"] = "Password:"
        self.password_label.pack()

        # create an entry field for the password
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # create a login button
        self.login_button = tk.Button(self)
        self.login_button["text"] = "Register"
        self.login_button["command"] = self.handle_register
        self.login_button.pack()

    def handle_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        
        user_data = {"Username": username, "Password": password, "Email": email, "Action": "register"}
        json_data = json.dumps(user_data)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 1234))

        client_socket.send(json_data.encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()

        print(response)

