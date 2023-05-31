import tkinter as tk
import socket
import json

class NewPass(tk.Frame):
    def __init__(self, master=None, username=None):
        super().__init__(master)
        self.master = master
        self.username = username
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        self.Url_label = tk.Label(self)
        self.Url_label["text"] = "URL:"
        self.Url_label.pack()

        self.url_entry = tk.Entry(self)
        self.url_entry.pack()

        self.password_label = tk.Label(self)
        self.password_label["text"] = "New Password:"
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.send_button = tk.Button(self)
        self.send_button["text"] = "send"
        self.send_button["command"] = self.handle_newPass
        self.send_button.pack()

    def handle_newPass(self):
        url = self.url_entry.get()
        password = self.password_entry.get()
        print(self.username)
        
        user_data = {"Url": url, "Password": password, "Owner": self.username, "Action": "insert"}
        json_data = json.dumps(user_data)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 1234))

        client_socket.send(json_data.encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()

        print(response)

        #add message to show succses
        self.master.destroy()


