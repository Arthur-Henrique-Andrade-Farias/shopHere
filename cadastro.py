import tkinter as tk
from tkinter import font as tkfont
from conexao_bd_users import create_connection, cadastrar_user

class CadastroPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configuração de fundo e fonte
        self.configure(bg="#2c3e50")
        self.custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

        # Título da página
        self.label_title = tk.Label(self, text="Cadastro", font=self.title_font, fg="white", bg="#2c3e50")
        self.label_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Campos de entrada com placeholders
        self.entry_nome = self.create_rounded_entry("Nome")
        self.entry_email = self.create_rounded_entry("Email")
        self.entry_password = self.create_rounded_entry("Password", show="*")

        # Posicionamento dos widgets de entrada
        self.entry_nome.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.entry_email.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.entry_password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Criação do frame para os botões
        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.button_signup = tk.Button(button_frame, text="Signup", command=self.signup, font=self.custom_font, bg="#1abc9c", fg="white")
        self.button_login = tk.Button(button_frame, text="Login", command=self.go_to_login, font=self.custom_font, bg="#3498db", fg="white")

        # Posicionamento dos botões dentro do frame
        self.button_signup.pack(side="left", padx=10)
        self.button_login.pack(side="right", padx=10)

        # Centralizar a página de cadastro
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def create_rounded_entry(self, placeholder, show=""):
        # Criação do frame com borda arredondada
        frame = tk.Frame(self, bg="#ecf0f1", bd=2, relief="flat")
        frame.grid_propagate(False)

        entry = tk.Entry(frame, font=self.custom_font, bd=0, highlightthickness=0, show=show)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_focus_in(event, e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(event, e, p))
        entry.pack(fill="both", padx=10, pady=5)

        frame.update_idletasks()
        frame.configure(width=entry.winfo_reqwidth() + 20, height=entry.winfo_reqheight() + 10)
        return frame

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if placeholder == "Password":
                entry.config(show="*")

    def on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Password":
                entry.config(show="")

    def go_to_login(self):
        self.controller.show_frame('LoginPage')

    def signup(self):
        connection = create_connection()
        
        if connection is None:
            return
        
        nome = self.entry_nome.winfo_children()[0].get()
        email = self.entry_email.winfo_children()[0].get()
        password = self.entry_password.winfo_children()[0].get()

        if cadastrar_user(connection, nome, email, password):
            self.controller.show_frame('LoginPage')
        else: 
            print("Não foi possível cadastrar")

# Exemplo de inicialização do aplicativo (parte externa à classe CadastroPage)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cadastro Page")

    # Configuração da tela
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    frame = CadastroPage(root, None)  # 'None' aqui é apenas um substituto; substitua pelo controlador real
    frame.pack(expand=True, fill="both")

    root.mainloop()
