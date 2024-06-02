import tkinter as tk
from lista_lojas_adm import ListaLojasAdm
from criar_loja import CriarLoja
from editar_loja import EditarLoja
from login import LoginPage
from cadastro import CadastroPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Lojas")
        self.frames = {}
        self.create_frames()
        self.show_frame('LoginPage')

    def create_frames(self):
        self.frames['ListaLojasAdm'] = ListaLojasAdm(parent=self, controller=self)
        self.frames['ListaLojasAdm'].grid(row=0, column=0, sticky="nsew")

        self.frames['CriarLoja'] = CriarLoja(parent=self, controller=self)
        self.frames['CriarLoja'].grid(row=0, column=0, sticky="nsew")

        self.frames['LoginPage'] = LoginPage(parent=self, controller=self)
        self.frames['LoginPage'].grid(row=0, column=0, sticky="nsew")

        self.frames['CadastroPage'] = CadastroPage(parent=self, controller=self)
        self.frames['CadastroPage'].grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name, loja_info=None):
        if page_name not in self.frames and page_name == 'EditarLoja':
            self.frames['EditarLoja'] = EditarLoja(parent=self, controller=self, loja_info=loja_info)
            self.frames['EditarLoja'].grid(row=0, column=0, sticky="nsew")
        elif page_name == 'ListaLojasAdm':
            self.frames['ListaLojasAdm'].refresh()
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
