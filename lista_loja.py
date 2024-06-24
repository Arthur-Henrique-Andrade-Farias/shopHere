import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from io import BytesIO
import requests
from conexao_bd_lojas import create_connection, read_lojas

class ListaLojas(tk.Frame):
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

        frame_create = tk.Frame(self, bg="#2c3e50")
        frame_create.pack(anchor=tk.NE, padx=10, pady=10)
        btn_logout = tk.Button(frame_create, text="Logout", command=self.logout, font=self.custom_font, bg="red", fg="white")
        btn_logout.pack()

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
    
    def logout(self):
        self.controller.logged_in = False
        self.controller.show_frame('LoginPage')
