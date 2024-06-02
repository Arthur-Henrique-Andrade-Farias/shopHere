import tkinter as tk
from conexao_bd_users import create_connection, verificar_login

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.authenticated = False
        self.isAdmin = False

        self.label_email = tk.Label(self, text="Email:")
        self.label_password = tk.Label(self, text="Password:")
        self.entry_email= tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_signup = tk.Button(self, text="Signup", command=self.go_to_signup)

        self.label_email.grid(row=0, column=0, sticky="e")
        self.label_password.grid(row=1, column=0, sticky="e")
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.button_login.grid(row=2, column=1)
        self.button_signup.grid(row=2, column=0, sticky="w")

    def go_to_signup(self):
        self.controller.show_frame('CadastroPage')

    def login(self):
        connection = create_connection()
        
        if connection is None:
            return

        email = self.entry_email.get()
        password = self.entry_password.get()

        user = verificar_login(connection, email, password)

        if(user):
            self.authenticated = True
            if(user[4] == 1):
                self.isAdmin = True
                self.controller.show_frame('ListaLojasAdm')
            else:
                print("mostrar alguma outra tela")
        else: 
            print("Login falhou. Verifique suas credenciais.")
        
