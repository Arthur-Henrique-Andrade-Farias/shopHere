import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from conexao_bd_lojas import create_connection, read_lojas
from excluir_loja import excluir_loja
from editar_loja import EditarLoja
from tkinter import font as tkfont

class ListaLojasAdm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.images = []
        self.configure(bg="#2c3e50")
        self.custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.create_widgets()

    def create_widgets(self):
        lojas = self.ler_lojas()

        # Frame principal para os botões no topo
        frame_top = tk.Frame(self, bg="#2c3e50")
        frame_top.pack(fill=tk.X, padx=10, pady=10)

        # Subframe para o botão "Criar Nova Loja" no canto superior esquerdo
        frame_create = tk.Frame(frame_top, bg="#2c3e50")
        frame_create.pack(side=tk.LEFT)
        btn_create = tk.Button(frame_create, text="Criar Nova Loja", command=lambda: self.controller.show_frame('CriarLoja'), font=self.custom_font, bg="green", fg="white")
        btn_create.pack(side=tk.LEFT, padx=5)

        # Subframe para o botão "Logout" no canto superior direito
        frame_logout = tk.Frame(frame_top, bg="#2c3e50")
        frame_logout.pack(side=tk.RIGHT)
        btn_logout = tk.Button(frame_logout, text="Logout", command=self.logout, font=self.custom_font, bg="red", fg="white")
        btn_logout.pack(side=tk.RIGHT, padx=5)

        # Frame para centralizar as lojas
        center_frame = tk.Frame(self, bg="#2c3e50")
        center_frame.pack(expand=True, pady=(20, 0))

        max_image_width = 200
        max_image_height = 200

        for loja in lojas:
            frame = tk.Frame(center_frame, bg="#34495e")
            frame.pack(padx=10, pady=10, anchor=tk.N)

            try:
                image = Image.open(loja[4])
                image = self.resize_image(image, max_image_width, max_image_height)

                tk_image = ImageTk.PhotoImage(image)
                self.images.append(tk_image)

                label_img = tk.Label(frame, image=tk_image, bg="#34495e")
                label_img.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            except Exception as e:
                print(f"Erro ao carregar imagem da loja {loja[1]}: {e}")

            label_info = tk.Label(frame, text=f"Nome: {loja[1]}\nDescrição: {loja[2]}\nMédia de Preço: {loja[3]}\nEndereço: {loja[5]}, {loja[6]}, {loja[7]}", fg="white", bg="#34495e", font=self.custom_font)
            label_info.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            btn_excluir = tk.Button(frame, text="Excluir", command=lambda id=loja[0], f=frame: self.excluir_loja_wrapper(id, f), font=self.custom_font, bg="#e74c3c", fg="white")
            btn_excluir.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            btn_editar = tk.Button(frame, text="Editar", command=lambda info=loja: self.controller.show_frame('EditarLoja', loja_info=info), font=self.custom_font, bg="#f39c12", fg="white")
            btn_editar.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    def ler_lojas(self):
        connection = create_connection()
        if connection is None:
            return []
        lojas = read_lojas(connection)
        connection.close()
        return lojas

    def resize_image(self, image, max_width, max_height):
        width, height = image.size
        if width > max_width or height > max_height:
            image.thumbnail((max_width, max_height), Image.LANCZOS)
        return image

    def excluir_loja_wrapper(self, loja_id, frame):
        excluir_loja(loja_id, frame)
        self.controller.update()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def logout(self):
        self.controller.logged_in = False
        self.controller.show_frame('LoginPage')
