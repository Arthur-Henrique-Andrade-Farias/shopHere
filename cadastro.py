import tkinter as tk
from conexao_bd_users import create_connection, cadastrar_user

class CadastroPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")

        container = tk.Frame(self, bg="#f0f0f0")
        container.place(relx=0.7, rely=0.5)

        self.label_nome = tk.Label(container, text="Nome:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_email = tk.Label(container, text="Email:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_password = tk.Label(container, text="Password:", font=('Helvetica', 12), bg="#f0f0f0")
        self.entry_nome = tk.Entry(container, font=('Helvetica', 12), bd=2, relief="groove")
        self.entry_email = tk.Entry(container, font=('Helvetica', 12), bd=2, relief="groove")
        self.entry_password = tk.Entry(container, show="*", font=('Helvetica', 12), bd=2, relief="groove")
        self.button_signup = tk.Button(container, text="Signup", command=self.signup, font=('Helvetica', 12), bg="#4CAF50", fg="white", relief="raised")
        self.button_login = tk.Button(container, text="Login", command=self.go_to_login, font=('Helvetica', 12), bg="#4CAF50", fg="white", relief="raised")

        self.label_nome.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.label_email.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.label_password.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)
        self.entry_email.grid(row=1, column=1, padx=10, pady=10)
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)
        self.button_signup.grid(row=3, column=1, sticky="e", pady=10)
        self.button_login.grid(row=3, column=0, sticky="w", pady=10)

    def go_to_login(self):
        self.controller.show_frame('LoginPage')

    def signup(self):
        connection = create_connection()
        
        if connection is None:
            print("Conexão ao MySQL falhou")
            return
        
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        if cadastrar_user(connection, nome, email, password):
            self.controller.show_frame('LoginPage')
        else: 
            print("Não foi possível cadastrar")
