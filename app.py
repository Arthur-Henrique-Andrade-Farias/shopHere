import tkinter as tk
from conexao_bd import create_connection
from lista_lojas import ListaLojas
from criar_loja import CriarLoja

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Lojas")
        self.frames = {}
        self.create_frames()
        self.show_frame('ListaLojas')

    def create_frames(self):
        for F in (ListaLojas, CriarLoja):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == 'ListaLojas':
            frame.refresh()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
