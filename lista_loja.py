import tkinter as tk
from tkinter import font as tkfont
from tkinter import Toplevel, Label, Button, Entry
from PIL import Image, ImageTk
from io import BytesIO
import requests
from conexao_bd_lojas import create_connection, read_lojas, read_itens

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

        # Canvas com barras de rolagem
        canvas = tk.Canvas(self, bg="#2c3e50")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollable_frame = tk.Frame(canvas, bg="#2c3e50")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        max_image_width = 200
        max_image_height = 200

        for loja in lojas:
            frame = tk.Frame(scrollable_frame, bg="#34495e")
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

            btn_view_items = tk.Button(frame, text="Ver Itens", command=lambda loja_id=loja[0]: self.mostrar_itens(loja_id), font=self.custom_font, bg="#3498db", fg="white")
            btn_view_items.grid(row=1, column=0, padx=10, pady=5, sticky="w")

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
    
    def mostrar_itens(self, loja_id):
        connection = create_connection()
        if connection is None:
            return

        itens = read_itens(connection, loja_id)
        connection.close()

        popup = Toplevel(self)
        popup.title("Itens da Loja")
        popup.configure(bg="#2c3e50")

        width = 600
        height = 400
        self.center_popup(popup, width, height)

        popup_frame = tk.Frame(popup, bg="#2c3e50")
        popup_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        for item in itens:
            item_frame = tk.Frame(popup_frame, bg="#34495e")
            item_frame.pack(padx=10, pady=10, fill=tk.X)

            label_item = tk.Label(item_frame, text=f"Nome: {item[1]}\nDescrição: {item[2]}\nValor: {item[3]}", fg="white", bg="#34495e", font=self.custom_font)
            label_item.pack(padx=10, pady=10, anchor=tk.CENTER)

            try:
                image = Image.open(item[4])
                image = self.resize_image(image, 100, 100)

                tk_image = ImageTk.PhotoImage(image)
                label_img = tk.Label(item_frame, image=tk_image, bg="#34495e")
                label_img.image = tk_image  # keep a reference
                label_img.pack(pady=10)
            except Exception as e:
                print(f"Erro ao carregar imagem do item {item[1]}: {e}")

    def logout(self):
        self.controller.logged_in = False
        self.controller.show_frame('LoginPage')

    def center_popup(self, popup, width, height):
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
