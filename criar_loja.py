import tkinter as tk
from tkinter import messagebox
from conexao_bd import create_connection, add_loja  

def criar_loja():
    form = tk.Toplevel()
    form.title("Criar Nova Loja")

    def salvar_nova_loja():
        nome = entry_nome.get()
        descricao = entry_descricao.get("1.0", tk.END)
        media_preco = entry_media_preco.get()
        url_img = entry_url_img.get()
        rua = entry_rua.get()
        bairro = entry_bairro.get()
        numero_endereco = entry_numero_endereco.get()

        connection = create_connection()

        if connection is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return
        
        add_loja(connection, nome, descricao, media_preco, url_img, rua, bairro, numero_endereco)
        connection.close()

        messagebox.showinfo("Sucesso", "Loja adicionada com sucesso")
        
        form.destroy()

    tk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(form)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Descrição:").grid(row=1, column=0, sticky="w")
    entry_descricao = tk.Text(form, height=4, width=30)
    entry_descricao.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form, text="Média de Preço:").grid(row=2, column=0, sticky="w")
    entry_media_preco = tk.Entry(form)
    entry_media_preco.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form, text="URL da Imagem:").grid(row=3, column=0, sticky="w")
    entry_url_img = tk.Entry(form)
    entry_url_img.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form, text="Rua:").grid(row=4, column=0, sticky="w")
    entry_rua = tk.Entry(form)
    entry_rua.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form, text="Bairro:").grid(row=5, column=0, sticky="w")
    entry_bairro = tk.Entry(form)
    entry_bairro.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form, text="Número do Endereço:").grid(row=6, column=0, sticky="w")
    entry_numero_endereco = tk.Entry(form)
    entry_numero_endereco.grid(row=6, column=1, padx=5, pady=5)

    btn_salvar = tk.Button(form, text="Salvar", command=salvar_nova_loja)
    btn_salvar.grid(row=7, columnspan=2, padx=5, pady=10)