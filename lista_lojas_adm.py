import tkinter as tk
from tkinter import font as tkfont, messagebox, filedialog, Toplevel, Label, Button, Entry, Text
from PIL import Image, ImageTk
from io import BytesIO
import requests
from conexao_bd_lojas import create_connection, read_lojas, read_itens, add_item
from excluir_loja import excluir_loja
from editar_loja import EditarLoja

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

        frame_top = tk.Frame(self, bg="#2c3e50")
        frame_top.pack(fill=tk.X, padx=10, pady=10)

        frame_create = tk.Frame(frame_top, bg="#2c3e50")
        frame_create.pack(side=tk.LEFT)
        btn_create = tk.Button(frame_create, text="Criar Nova Loja", command=lambda: self.controller.show_frame('CriarLoja'), font=self.custom_font, bg="green", fg="white")
        btn_create.pack(side=tk.LEFT, padx=5)

        frame_logout = tk.Frame(frame_top, bg="#2c3e50")
        frame_logout.pack(side=tk.RIGHT)
        btn_logout = tk.Button(frame_logout, text="Logout", command=self.logout, font=self.custom_font, bg="red", fg="white")
        btn_logout.pack(side=tk.RIGHT, padx=5)

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

            btn_excluir = tk.Button(frame, text="Excluir", command=lambda id=loja[0], f=frame: self.excluir_loja_wrapper(id, f), font=self.custom_font, bg="#e74c3c", fg="white")
            btn_excluir.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            btn_editar = tk.Button(frame, text="Editar", command=lambda info=loja: self.controller.show_frame('EditarLoja', loja_info=info), font=self.custom_font, bg="#f39c12", fg="white")
            btn_editar.grid(row=1, column=1, padx=10, pady=5, sticky="e")

            btn_view_items = tk.Button(frame, text="Ver Itens", command=lambda loja_id=loja[0]: self.mostrar_itens(loja_id), font=self.custom_font, bg="#3498db", fg="white")
            btn_view_items.grid(row=2, column=0, padx=10, pady=5, sticky="w")

            btn_add_item = tk.Button(frame, text="Adicionar Item", command=lambda loja_id=loja[0]: self.adicionar_item(loja_id), font=self.custom_font, bg="#2ecc71", fg="white")
            btn_add_item.grid(row=2, column=1, padx=10, pady=5, sticky="e")

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

    def adicionar_item(self, loja_id):
        popup = Toplevel(self)
        popup.title("Adicionar Item")
        popup.configure(bg="#2c3e50")

        width = 400
        height = 400
        self.center_popup(popup, width, height)

        self.image_path = ""

        label_nome = tk.Label(popup, text="Nome:", font=self.custom_font, fg="white", bg="#2c3e50")
        label_nome.pack(pady=5)
        frame_nome, entry_nome = self.create_rounded_entry(popup, "Nome")
        frame_nome.pack(pady=5)

        label_descricao = tk.Label(popup, text="Descrição:", font=self.custom_font, fg="white", bg="#2c3e50")
        label_descricao.pack(pady=5)
        frame_descricao, entry_descricao = self.create_rounded_text(popup, "Descrição", height=4)
        frame_descricao.pack(pady=5)

        label_valor = tk.Label(popup, text="Valor:", font=self.custom_font, fg="white", bg="#2c3e50")
        label_valor.pack(pady=5)
        frame_valor, entry_valor = self.create_rounded_entry(popup, "Valor")
        frame_valor.pack(pady=5)

        button_select_img = tk.Button(popup, text="Selecionar Imagem", command=self.selecionar_imagem, font=self.custom_font, bg="blue", fg="white")
        button_select_img.pack(pady=5)

        def submit_item():
            nome = entry_nome.get()
            descricao = entry_descricao.get("1.0", tk.END).strip()
            valor = entry_valor.get()

            if not self.image_path:
                messagebox.showerror("Erro", "Por favor, selecione uma imagem para o item.")
                return

            connection = create_connection()
            if connection is None:
                return

            add_item(connection, nome, descricao, valor, self.image_path, loja_id)
            connection.close()

            popup.destroy()
            self.refresh()

        btn_submit = tk.Button(popup, text="Adicionar", command=submit_item, font=self.custom_font, bg="#2ecc71", fg="white")
        btn_submit.pack(pady=20)

    def create_rounded_entry(self, parent, placeholder, show=""):
        frame = tk.Frame(parent, bg="#ecf0f1", bd=2, relief="flat")
        frame.grid_propagate(False)

        entry = tk.Entry(frame, font=self.custom_font, bd=0, highlightthickness=0, show=show)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_focus_in(event, e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(event, e, p))
        entry.pack(fill="both", padx=10, pady=5)

        frame.update_idletasks()
        frame.configure(width=entry.winfo_reqwidth() + 20, height=entry.winfo_reqheight() + 10)
        return frame, entry

    def create_rounded_text(self, parent, placeholder, height=4):
        frame = tk.Frame(parent, bg="#ecf0f1", bd=2, relief="flat")
        frame.grid_propagate(False)

        text = tk.Text(frame, font=self.custom_font, bd=0, highlightthickness=0, height=height)
        text.insert("1.0", placeholder)
        text.bind("<FocusIn>", lambda event, t=text, p=placeholder: self.on_focus_in_text(event, t, p))
        text.bind("<FocusOut>", lambda event, t=text, p=placeholder: self.on_focus_out_text(event, t, p))
        text.pack(fill="both", padx=10, pady=5)

        frame.update_idletasks()
        frame.configure(width=text.winfo_reqwidth() + 20, height=text.winfo_reqheight() + 10)
        return frame, text

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

    def center_popup(self, popup, width, height):
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
