import tkinter as tk
from conexao_bd import create_connection, update_loja  

def editar_loja(loja_info):
    root = tk.Toplevel() 
    root.title("Editar Loja")
    print(loja_info[1])

    nome_var = tk.StringVar(value=loja_info[1])
    descricao_var = tk.StringVar(value=loja_info[2])
    media_preco_var = tk.StringVar(value=loja_info[3])
    url_img_var = tk.StringVar(value=loja_info[4])
    rua_var = tk.StringVar(value=loja_info[5])
    bairro_var = tk.StringVar(value=loja_info[6])
    numero_endereco_var = tk.StringVar(value=loja_info[7])

    tk.Label(root, text="Nome:").grid(row=0, column=0)
    tk.Entry(root, textvariable=nome_var).grid(row=0, column=1)

    tk.Label(root, text="Descrição:").grid(row=1, column=0)
    tk.Entry(root, textvariable=descricao_var).grid(row=1, column=1)

    tk.Label(root, text="Média de Preço:").grid(row=2, column=0)
    tk.Entry(root, textvariable=media_preco_var).grid(row=2, column=1)

    tk.Label(root, text="URL da Imagem:").grid(row=3, column=0)
    tk.Entry(root, textvariable=url_img_var).grid(row=3, column=1)

    tk.Label(root, text="Rua:").grid(row=4, column=0)
    tk.Entry(root, textvariable=rua_var).grid(row=4, column=1)

    tk.Label(root, text="Bairro:").grid(row=5, column=0)
    tk.Entry(root, textvariable=bairro_var).grid(row=5, column=1)

    tk.Label(root, text="Número do Endereço:").grid(row=6, column=0)
    tk.Entry(root, textvariable=numero_endereco_var).grid(row=6, column=1)

    def salvar_edicao():
        connection = create_connection()

        if connection is None:
            return

        update_loja(connection, loja_info[0],
                    nome=nome_var.get(),
                    descricao=descricao_var.get(),
                    media_preco=media_preco_var.get(),
                    url_img=url_img_var.get(),
                    rua=rua_var.get(),
                    bairro=bairro_var.get(),
                    numero_endereco=numero_endereco_var.get())
        
        connection.close()

        print("Loja atualizada com sucesso")

        root.destroy()

    btn_salvar = tk.Button(root, text="Salvar", command=salvar_edicao)
    btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()
