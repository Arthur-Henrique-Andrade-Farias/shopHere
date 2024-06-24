import tkinter as tk
from tkinter import font as tkfont, messagebox, filedialog
from conexao_bd_lojas import create_connection, add_loja

class CriarLoja(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_path = ""

        # Configuração de fundo e fonte
        self.configure(bg="#2c3e50")
        self.custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

        # Título da página
        self.label_title = tk.Label(self, text="Criar Nova Loja", font=self.title_font, fg="white", bg="#2c3e50")
        self.label_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Campos de entrada com placeholders
        self.entry_nome = self.create_rounded_entry("Nome")
        self.entry_descricao = self.create_rounded_text("Descrição", height=4)
        self.entry_media_preco = self.create_rounded_entry("Média de Preço")
        self.entry_rua = self.create_rounded_entry("Rua")
        self.entry_bairro = self.create_rounded_entry("Bairro")
        self.entry_numero_endereco = self.create_rounded_entry("Número do Endereço")

        # Botão para selecionar imagem
        self.btn_image = tk.Button(self, text="Selecionar Imagem", command=self.selecionar_imagem, font=self.custom_font, bg="blue", fg="white")
        self.btn_image.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Label para exibir o caminho da imagem selecionada
        self.label_image_path = tk.Label(self, text="", font=self.custom_font, fg="white", bg="#2c3e50")
        self.label_image_path.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Posicionamento dos widgets de entrada
        self.entry_nome.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.entry_descricao.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.entry_media_preco.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.entry_rua.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.entry_bairro.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.entry_numero_endereco.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Criação do frame para os botões
        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        # Botão de salvar
        self.button_save = tk.Button(button_frame, text="Salvar", command=self.salvar_nova_loja, font=self.custom_font, bg="#1abc9c", fg="white")
        self.button_save.pack(side="left", padx=10)

        # Botão de voltar
        self.button_back = tk.Button(button_frame, text="Voltar para Lista", command=self.voltar_para_lista, font=self.custom_font, bg="#e74c3c", fg="white")
        self.button_back.pack(side="left", padx=10)

        # Centralizar a página de criação de loja
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)

    def create_rounded_entry(self, placeholder, show=""):
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

    def create_rounded_text(self, placeholder, height=4):
        frame = tk.Frame(self, bg="#ecf0f1", bd=2, relief="flat")
        frame.grid_propagate(False)

        text = tk.Text(frame, font=self.custom_font, bd=0, highlightthickness=0, height=height)
        text.insert("1.0", placeholder)
        text.bind("<FocusIn>", lambda event, t=text, p=placeholder: self.on_focus_in_text(event, t, p))
        text.bind("<FocusOut>", lambda event, t=text, p=placeholder: self.on_focus_out_text(event, t, p))
        text.pack(fill="both", padx=10, pady=5)

        frame.update_idletasks()
        frame.configure(width=text.winfo_reqwidth() + 20, height=text.winfo_reqheight() + 10)
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

    def on_focus_in_text(self, event, text, placeholder):
        if text.get("1.0", tk.END).strip() == placeholder:
            text.delete("1.0", tk.END)

    def on_focus_out_text(self, event, text, placeholder):
        if text.get("1.0", tk.END).strip() == "":
            text.insert("1.0", placeholder)

    def selecionar_imagem(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path = file_path
            self.label_image_path.config(text=file_path)

    def salvar_nova_loja(self):
        nome = self.entry_nome.winfo_children()[0].get()
        descricao = self.entry_descricao.winfo_children()[0].get("1.0", tk.END)
        media_preco = self.entry_media_preco.winfo_children()[0].get()
        rua = self.entry_rua.winfo_children()[0].get()
        bairro = self.entry_bairro.winfo_children()[0].get()
        numero_endereco = self.entry_numero_endereco.winfo_children()[0].get()

        if not self.image_path:
            messagebox.showerror("Erro", "Por favor, selecione uma imagem para a loja.")
            return

        connection = create_connection()

        if connection is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return

        # Armazenar o caminho da imagem no banco de dados
        add_loja(connection, nome, descricao, media_preco, self.image_path, rua, bairro, numero_endereco)
        connection.close()

        messagebox.showinfo("Sucesso", "Loja adicionada com sucesso")

    def voltar_para_lista(self):
        self.controller.show_frame('ListaLojasAdm')
