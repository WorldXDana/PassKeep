import tkinter as tk
#from LoginScreen import LoginScreen
from NewPass import NewPass
import json
import socket

class ListPasswords(tk.Frame):
    def __init__(self, master=None, username=None, objects=None):
        super().__init__(master)
        self.master = master
        self.username = username
        print(username)
        self.master.configure(bg="#000000")
        self.pack(fill="both", expand=True)
        self.create_widgets(objects)

    def create_widgets(self, objects):
        self.left_frame = tk.Frame(self, width=0.3*self.master.winfo_screenwidth(), bg="#303030")
        self.left_frame.pack(side="left", fill="both")

        self.right_frame = tk.Frame(self, bg="#000000")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.create_buttons_labels()
        self.create_object_list(self.get_passwords())

    def create_buttons_labels(self):
        self.buttons_labels = []
        button_texts = ["New Password", "Logout", "refresh"]
        label_texts = [["Label 1a", "Label 1b"], ["Label 2a", "Label 2b"]]

        for i in range(len(button_texts)):
            button = tk.Button(
                self.left_frame,
                text=button_texts[i],
                width=10,
                height=5,
                relief="flat",
                bd=0,
                bg="#CCCCCC",
                activebackground="#AAAAAA",
                padx=10,
                pady=10,
                borderwidth=0,
                command=lambda i=i: self.handle_button_click(i)
            )
            button.pack(padx=10, pady=10)
            self.buttons_labels.append((button, []))

    def get_passwords(self):
        temp = [{"Url": "hello", "Password": "world!"},
                {"Url": "hello", "Password": "world!"}]
        
        user_data = {"Username": self.username, "Action": "getAllPasses"} 
        json_data = json.dumps(user_data)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 1234))
        client_socket.send(json_data.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        client_socket.close()

        return json.loads(response)
        
    def create_object_list(self, objects):
        #print(objects)
        self.object_list = tk.Listbox(self.right_frame)
        self.object_list.config(relief="flat", bg="#000000", fg="#FFFFFF")
        if objects:
            for obj in objects:
                self.object_list.insert(tk.END, "Url: " + obj["Url"])
                self.object_list.insert(tk.END, "Password: " + obj["Password"])
                self.object_list.insert(tk.END, "-" * 200)  # Thin line separator
        self.object_list.pack(side="left", fill="both", expand=True)

    def update_object_list(self, objects):
        self.object_list.delete(0, tk.END)
        if objects:
            for obj in objects:
                self.object_list.insert(tk.END, "Url: " + obj["Url"])
                self.object_list.insert(tk.END, "Password: " + obj["Password"])
                self.object_list.insert(tk.END, "-" * 200)  # Thin line separator
            self.object_list.pack(side="left", fill="both", expand=True)

    def handle_button_click(self, button_index):
        button_text = self.buttons_labels[button_index][0]["text"]
        print(f"Button {button_index + 1} clicked. Text: {button_text}")
        if button_index == 0:
            self.handle_newPass()
        if button_index == 1:
            self.handle_logout()
        if button_index == 2:
            self.handle_refresh()
        
    def handle_refresh(self):
        try:
            self.master.destroy()
            ListPasswords_window = tk.Tk()
            ListPasswords_window.title(self.username + "'s passwords")
            ListPasswords_screen = ListPasswords(ListPasswords_window, self.username)
            ListPasswords_screen.mainloop()
        except Exception as e:
            pass


    def handle_newPass(self):
        newPass_window = tk.Toplevel()
        newPass_window.title("Enter A New Password")
        newPass_screen = NewPass(newPass_window, self.username)
        newPass_screen.mainloop()
        print("were on")
        self.update_object_list(self.get_passwords())

    def handle_logout(self):
        user_data = {"Username": self.username, "Action": "logout"}
        json_data = json.dumps(user_data)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 1234))

        client_socket.send(json_data.encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()

        print(response)

        try:
            if response == str("user " + self.username + " has logged out"):
                print("logout was a success")
                self.master.destroy()
            else:
                print("logout failed")
        except Exception as e:
            pass

    def start(self):
        self.master.mainloop()