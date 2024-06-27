import tkinter as tk
from tkinter import font as tkfont, messagebox, filedialog, Toplevel
from conexao_bd_lojas import create_connection, add_loja, read_cidades, add_cidade

class CriarLoja(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_path = ""
        self.cidades = self.ler_cidades()
        self.cidade_selecionada = tk.StringVar(value=self.cidades[0][1] if self.cidades else "")

        # Configuração de fundo e fonte
        self.configure(bg="#2c3e50")
        self.custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

        # Título da página
        self.label_title = tk.Label(self, text="Criar Nova Loja", font=self.title_font, fg="white", bg="#2c3e50")
        self.label_title.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Campo para selecionar a cidade
        self.label_cidade = tk.Label(self, text="Cidade Selecionada:", font=self.custom_font, fg="white", bg="#2c3e50")
        self.label_cidade.grid(row=1, column=0, pady=(10, 5), sticky="w")

        self.option_menu_cidade = tk.OptionMenu(self, self.cidade_selecionada, *[cidade[1] for cidade in self.cidades])
        self.option_menu_cidade.grid(row=1, column=1, pady=(10, 5), sticky="e")

        if self.controller.logged_in_user and self.controller.logged_in_user['isAdmin']:
            self.btn_add_cidade = tk.Button(self, text="Adicionar Cidade", command=self.adicionar_cidade, font=self.custom_font, bg="green", fg="white")
            self.btn_add_cidade.grid(row=1, column=2, pady=(10, 5), padx=10)

        # Campos de entrada com placeholders
        self.entry_nome = self.create_rounded_entry("Nome")
        self.entry_descricao = self.create_rounded_text("Descrição", height=4)
        self.entry_media_preco = self.create_rounded_entry("Média de Preço")
        self.entry_rua = self.create_rounded_entry("Rua")
        self.entry_bairro = self.create_rounded_entry("Bairro")
        self.entry_numero_endereco = self.create_rounded_entry("Número do Endereço")

        # Botão para selecionar imagem
        self.btn_image = tk.Button(self, text="Selecionar Imagem", command=self.selecionar_imagem, font=self.custom_font, bg="blue", fg="white")
        self.btn_image.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Label para exibir o caminho da imagem selecionada
        self.label_image_path = tk.Label(self, text="", font=self.custom_font, fg="white", bg="#2c3e50")
        self.label_image_path.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Posicionamento dos widgets de entrada
        self.entry_nome.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.entry_descricao.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.entry_media_preco.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        self.entry_rua.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        self.entry_bairro.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        self.entry_numero_endereco.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

        # Criação do frame para os botões
        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.grid(row=10, column=0, columnspan=3, pady=10)

        # Botão de salvar
        self.button_save = tk.Button(button_frame, text="Salvar", command=self.salvar_nova_loja, font=self.custom_font, bg="#1abc9c", fg="white")
        self.button_save.pack(side="left", padx=10)

        # Botão de voltar
        self.button_back = tk.Button(button_frame, text="Voltar para Lista", command=self.voltar_para_lista, font=self.custom_font, bg="#e74c3c", fg="white")
        self.button_back.pack(side="left", padx=10)

        # Centralizar a página de criação de loja
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
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
        self.grid_rowconfigure(10, weight=1)

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
        cidade_nome = self.cidade_selecionada.get()

        if not self.image_path:
            messagebox.showerror("Erro", "Por favor, selecione uma imagem para a loja.")
            return

        connection = create_connection()
        if connection is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM cidades WHERE nome = %s", (cidade_nome,))
        cidade_id = cursor.fetchone()[0]

        add_loja(connection, nome, descricao, media_preco, self.image_path, rua, bairro, numero_endereco, cidade_id)
        connection.close()

        messagebox.showinfo("Sucesso", "Loja adicionada com sucesso")

    def voltar_para_lista(self):
        self.controller.show_frame('ListaLojasAdm')

    def ler_cidades(self):
        connection = create_connection()
        if connection is None:
            return []
        cidades = read_cidades(connection)
        connection.close()
        return cidades

    def adicionar_cidade(self):
        popup = Toplevel(self)
        popup.title("Adicionar Cidade")
        popup.configure(bg="#2c3e50")

        label_nome = tk.Label(popup, text="Nome da Cidade:", font=self.custom_font, fg="white", bg="#2c3e50")
        label_nome.pack(pady=5)
        entry_nome = tk.Entry(popup, font=self.custom_font)
        entry_nome.pack(pady=5)

        label_estado = tk.Label(popup, text="Estado:", font=self.custom_font, fg="white", bg="#2c3e50")
        label_estado.pack(pady=5)
        entry_estado = tk.Entry(popup, font=self.custom_font)
        entry_estado.pack(pady=5)

        def submit_cidade():
            nome = entry_nome.get()
            estado = entry_estado.get()
            if nome and estado:
                connection = create_connection()
                add_cidade(connection, nome, estado)
                connection.close()
                popup.destroy()
                self.refresh_cidades()

        btn_submit = tk.Button(popup, text="Adicionar", command=submit_cidade, font=self.custom_font, bg="green", fg="white")
        btn_submit.pack(pady=20)

    def refresh_cidades(self):
        self.cidades = self.ler_cidades()
        self.option_menu_cidade['menu'].delete(0, 'end')
        for cidade in self.cidades:
            self.option_menu_cidade['menu'].add_command(label=cidade[1], command=tk._setit(self.cidade_selecionada, cidade[1]))
