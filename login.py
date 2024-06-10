import tkinter as tk
from conexao_bd_users import create_connection, verificar_login

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.authenticated = False
        self.isAdmin = False
        self.configure(bg="#f0f0f0")

        container = tk.Frame(self, bg="#f0f0f0")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_email = tk.Label(container, text="Email:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_password = tk.Label(container, text="Password:", font=('Helvetica', 12), bg="#f0f0f0")
        self.entry_email = tk.Entry(container, font=('Helvetica', 12), bd=2, relief="groove")
        self.entry_password = tk.Entry(container, show="*", font=('Helvetica', 12), bd=2, relief="groove")
        self.button_login = tk.Button(container, text="Login", command=self.login, font=('Helvetica', 12), bg="#4CAF50", fg="white", relief="raised")
        self.button_signup = tk.Button(container, text="Signup", command=self.go_to_signup, font=('Helvetica', 12), bg="#4CAF50", fg="white", relief="raised")

        self.label_email.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.label_password.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_email.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        self.button_login.grid(row=2, column=1, pady=10, sticky="e")
        self.button_signup.grid(row=2, column=0, pady=10, sticky="w")

    def go_to_signup(self):
        self.controller.show_frame('CadastroPage')

    def login(self):
        connection = create_connection()
        
        if connection is None:
            print("Conexão ao MySQL falhou")
            return

        email = self.entry_email.get()
        password = self.entry_password.get()

        user = verificar_login(connection, email, password)

        if user:
            self.authenticated = True
            self.controller.logged_in = True
            if user[4] == 1:
                self.isAdmin = True
                self.controller.show_frame('ListaLojasAdm')
            else:
                self.controller.show_frame('ListaLojas')
        else: 
            print("Login falhou. Verifique suas credenciais.")
