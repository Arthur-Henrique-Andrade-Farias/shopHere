import tkinter as tk
from conexao_bd_lojas import create_connection, update_loja

class EditarLoja(tk.Frame):
    def __init__(self, parent, controller, loja_info):
        super().__init__(parent)
        self.controller = controller
        self.loja_info = loja_info
        self.create_widgets()

    def create_widgets(self):
        loja_info = self.loja_info
        
        tk.Label(self, text="Editar Loja", font=('Helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Button(self, text="Voltar para Lista", command=lambda: self.controller.show_frame('ListaLojas')).grid(row=1, column=0, columnspan=2, pady=5)

        nome_var = tk.StringVar(value=loja_info[1])
        descricao_var = tk.StringVar(value=loja_info[2])
        media_preco_var = tk.StringVar(value=loja_info[3])
        url_img_var = tk.StringVar(value=loja_info[4])
        rua_var = tk.StringVar(value=loja_info[5])
        bairro_var = tk.StringVar(value=loja_info[6])
        numero_endereco_var = tk.StringVar(value=loja_info[7])

        tk.Label(self, text="Nome:").grid(row=2, column=0)
        tk.Entry(self, textvariable=nome_var).grid(row=2, column=1)

        tk.Label(self, text="Descrição:").grid(row=3, column=0)
        tk.Entry(self, textvariable=descricao_var).grid(row=3, column=1)

        tk.Label(self, text="Média de Preço:").grid(row=4, column=0)
        tk.Entry(self, textvariable=media_preco_var).grid(row=4, column=1)

        tk.Label(self, text="URL da Imagem:").grid(row=5, column=0)
        tk.Entry(self, textvariable=url_img_var).grid(row=5, column=1)

        tk.Label(self, text="Rua:").grid(row=6, column=0)
        tk.Entry(self, textvariable=rua_var).grid(row=6, column=1)

        tk.Label(self, text="Bairro:").grid(row=7, column=0)
        tk.Entry(self, textvariable=bairro_var).grid(row=7, column=1)

        tk.Label(self, text="Número do Endereço:").grid(row=8, column=0)
        tk.Entry(self, textvariable=numero_endereco_var).grid(row=8, column=1)

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
            self.controller.show_frame('ListaLojas')

        tk.Button(self, text="Salvar", command=salvar_edicao).grid(row=9, column=0, columnspan=2, pady=10)
