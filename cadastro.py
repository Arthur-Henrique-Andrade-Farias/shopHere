import tkinter as tk
from conexao_bd_users import create_connection, cadastrar_user

class CadastroPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_nome = tk.Label(self, text="Nome:")
        self.label_email = tk.Label(self, text="Email:")
        self.label_password = tk.Label(self, text="Password:")
        self.entry_nome = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.button_signup = tk.Button(self, text="Signup", command=self.signup)
        self.button_login = tk.Button(self, text="Login", command=self.go_to_login)

        self.label_nome.grid(row=0, column=0, sticky="e")
        self.label_email.grid(row=1, column=0, sticky="e")
        self.label_password.grid(row=2, column=0, sticky="e")
        self.entry_nome.grid(row=0, column=1)
        self.entry_email.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        self.button_signup.grid(row=3, column=1, sticky="e")
        self.button_login.grid(row=3, column=1, sticky="w")

    def go_to_login(self):
        self.controller.show_frame('LoginPage')

    def signup(self):
        connection = create_connection()
        
        if connection is None:
            return
        
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        if(cadastrar_user(connection, nome, email, password)):
            self.controller.show_frame('LoginPage')
        else: 
            print("Não foi possível cadastrar")

