import tkinter as tk
import socket
import json
from ListPasswords import ListPasswords
from SignUp import SignUp

class LoginScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # create a label for the username field
        self.username_label = tk.Label(self)
        self.username_label["text"] = "Username:"
        self.username_label.pack()

        # create an entry field for the username
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # create a label for the password field
        self.password_label = tk.Label(self)
        self.password_label["text"] = "Password:"
        self.password_label.pack()

        # create an entry field for the password
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # create a login button
        self.login_button = tk.Button(self)
        self.login_button["text"] = "Login"
        self.login_button["command"] = self.handle_login
        self.login_button.pack()

        # create a signup button
        self.signup_button = tk.Button(self)
        self.signup_button["text"] = "register"
        self.signup_button["command"] = self.go_to_signup
        self.signup_button.pack()

    def handle_login(self):
        # get the username and password from the entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # create a dictionary with the username and password
        login_data = {"Username": username, "Password": password, "Action": "login"}

        # convert the dictionary to a JSON string
        json_data = json.dumps(login_data)

        # create a socket connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 1234))

        # send the JSON string to the server
        client_socket.send(json_data.encode())

        # receive the response from the server
        response = client_socket.recv(1024).decode()

        # close the socket connection
        client_socket.close()

        # print the response to the console
        print(response)

        if(response == f"Hello, I received your message!"):
            self.master.destroy()
            ListPasswords_window = tk.Tk()
            ListPasswords_window.title(username + "'s passwords")
            ListPasswords_screen = ListPasswords(ListPasswords_window, username)
            ListPasswords_screen.mainloop()
        else:
            print("login couldn't happen")

    def go_to_signup(self):
        signup_window = tk.Toplevel()
        signup_window.title("register")
        signup_screen = SignUp(signup_window)
        signup_screen.mainloop()