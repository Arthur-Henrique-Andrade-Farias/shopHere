import tkinter as tk
from tkinter import messagebox
from conexao_bd_lojas import create_connection, add_loja

class CriarLoja(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Criar Nova Loja", font=('Helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        btn_back = tk.Button(self, text="Voltar para Lista", command=self.voltar_para_lista)
        btn_back.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Label(self, text="Nome:").grid(row=2, column=0, sticky="w")
        self.entry_nome = tk.Entry(self)
        self.entry_nome.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Descrição:").grid(row=3, column=0, sticky="w")
        self.entry_descricao = tk.Text(self, height=4, width=30)
        self.entry_descricao.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Média de Preço:").grid(row=4, column=0, sticky="w")
        self.entry_media_preco = tk.Entry(self)
        self.entry_media_preco.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="URL da Imagem:").grid(row=5, column=0, sticky="w")
        self.entry_url_img = tk.Entry(self)
        self.entry_url_img.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self, text="Rua:").grid(row=6, column=0, sticky="w")
        self.entry_rua = tk.Entry(self)
        self.entry_rua.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="Bairro:").grid(row=7, column=0, sticky="w")
        self.entry_bairro = tk.Entry(self)
        self.entry_bairro.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self, text="Número do Endereço:").grid(row=8, column=0, sticky="w")
        self.entry_numero_endereco = tk.Entry(self)
        self.entry_numero_endereco.grid(row=8, column=1, padx=5, pady=5)

        btn_salvar = tk.Button(self, text="Salvar", command=self.salvar_nova_loja)
        btn_salvar.grid(row=9, column=0, columnspan=2, padx=5, pady=10)

    def salvar_nova_loja(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get("1.0", tk.END)
        media_preco = self.entry_media_preco.get()
        url_img = self.entry_url_img.get()
        rua = self.entry_rua.get()
        bairro = self.entry_bairro.get()
        numero_endereco = self.entry_numero_endereco.get()

        connection = create_connection()

        if connection is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return
        
        add_loja(connection, nome, descricao, media_preco, url_img, rua, bairro, numero_endereco)
        connection.close()

        messagebox.showinfo("Sucesso", "Loja adicionada com sucesso")

    def voltar_para_lista(self):
        self.controller.show_frame('ListaLojas')
