import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from conexao_bd import create_connection, read_lojas
from excluir_loja import excluir_loja
from editar_loja import editar_loja
from criar_loja import criar_loja

root = tk.Tk()

def resize_image(image, max_width, max_height):
    width, height = image.size
    if width > max_width or height > max_height:
        image.thumbnail((max_width, max_height), Image.LANCZOS)
    return image

def ler_lojas():
    connection = create_connection()

    if connection is None:
        return []

    lojas = read_lojas(connection)
    connection.close()

    return lojas

def excluir_loja_wrapper(loja_id, frame):
    excluir_loja(loja_id, frame)
    root.update()

def editar_loja_wrapper(info): 
    editar_loja(info)
    root.update()

def criar_loja_wrapper():
    criar_loja()

def criar_botao_adicionar():
    frame_create = tk.Frame(root)
    frame_create.pack(anchor=tk.NE, padx=10, pady=10)
    btn_create = tk.Button(frame_create, text="Criar Nova Loja", command=criar_loja_wrapper, bg="green", fg="white")
    btn_create.pack()

def show_lojas():
    lojas = ler_lojas()

    root.title("Lista de Lojas")

    max_image_width = 200
    max_image_height = 200

    images = []

    criar_botao_adicionar()

    for loja in lojas:
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10, anchor=tk.W)

        try:
            response = requests.get(loja[4])

            image_bytes = BytesIO(response.content)
            image = Image.open(image_bytes)
            image = resize_image(image, max_image_width, max_image_height)

            tk_image = ImageTk.PhotoImage(image)
            images.append(tk_image) 

            label_img = tk.Label(frame, image=tk_image)
            label_img.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        except Exception as e:
            print(f"Erro ao carregar imagem da loja {loja[1]}: {e}")

        label_info = tk.Label(frame, text=f"Nome: {loja[1]}\nDescrição: {loja[2]}\nMédia de Preço: {loja[3]}\nEndereço: {loja[5]}, {loja[6]}, {loja[7]}")
        label_info.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        btn_excluir = tk.Button(frame, text="Excluir", command=lambda id=loja[0], f=frame: excluir_loja_wrapper(id, f))
        btn_excluir.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        btn_editar = tk.Button(frame, text="Editar", command=lambda info=loja: editar_loja_wrapper(info))
        btn_editar.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    root.mainloop()

if __name__ == "__main__":
    show_lojas()
