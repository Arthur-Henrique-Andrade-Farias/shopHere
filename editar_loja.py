import tkinter as tk
from tkinter import font as tkfont
from conexao_bd_lojas import create_connection, update_loja

class EditarLoja(tk.Frame):
    def __init__(self, parent, controller, loja_info):
        super().__init__(parent)
        self.controller = controller
        self.loja_info = loja_info
        self.configure(bg="#2c3e50")
        self.custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.create_widgets()

    def create_widgets(self):
        loja_info = self.loja_info

        tk.Label(self, text="Editar Loja", font=self.title_font, fg="white", bg="#2c3e50").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Voltar para Lista", command=lambda: self.controller.show_frame('ListaLojasAdm'), font=self.custom_font, bg="#3498db", fg="white").grid(row=1, column=0, columnspan=2, pady=5)

        self.create_label_and_entry("Nome:", loja_info[1], 2)
        self.create_label_and_entry("Descrição:", loja_info[2], 3)
        self.create_label_and_entry("Média de Preço:", loja_info[3], 4)
        self.create_label_and_entry("URL da Imagem:", loja_info[4], 5)
        self.create_label_and_entry("Rua:", loja_info[5], 6)
        self.create_label_and_entry("Bairro:", loja_info[6], 7)
        self.create_label_and_entry("Número do Endereço:", loja_info[7], 8)

        tk.Button(self, text="Salvar", command=self.salvar_edicao, font=self.custom_font, bg="#1abc9c", fg="white").grid(row=9, column=0, columnspan=2, pady=10)

    def create_label_and_entry(self, text, value, row):
        tk.Label(self, text=text, font=self.custom_font, fg="white", bg="#2c3e50").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        entry_var = tk.StringVar(value=value)
        entry = tk.Entry(self, textvariable=entry_var, font=self.custom_font)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
        setattr(self, f"entry_{text.split()[0].lower()}", entry_var)

    def salvar_edicao(self):
        loja_info = self.loja_info

        connection = create_connection()
        if connection is None:
            return

        update_loja(connection, loja_info[0],
                    nome=self.entry_nome.get(),
                    descricao=self.entry_descricao.get(),
                    media_preco=self.entry_media_preco.get(),
                    url_img=self.entry_url.get(),
                    rua=self.entry_rua.get(),
                    bairro=self.entry_bairro.get(),
                    numero_endereco=self.entry_numero.get())
        
        connection.close()

        print("Loja atualizada com sucesso")
        self.controller.show_frame('ListaLojasAdm')
