import tkinter as tk
from lista_lojas_adm import ListaLojasAdm
from criar_loja import CriarLoja
from editar_loja import EditarLoja
from lista_loja import ListaLojas
from login import LoginPage
from cadastro import CadastroPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Lojas")
        self.geometry("800x600")  # Defina as dimensões da janela aqui
        self.center_window()  # Centralizar a janela
        self.frames = {}
        self.logged_in = False
        self.logged_in_user = None
        self.create_frames()
        self.show_frame('LoginPage')

    def center_window(self):
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def create_frames(self):
        for F in (ListaLojasAdm, CriarLoja, LoginPage, CadastroPage, ListaLojas):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Certifique-se de que a janela principal expanda os frames corretamente
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_frame(self, page_name, loja_info=None):
        if not self.logged_in:
            if page_name not in ['LoginPage', 'CadastroPage']:
                page_name = 'LoginPage'

        if page_name not in self.frames and page_name == 'EditarLoja':
            self.frames['EditarLoja'] = EditarLoja(parent=self, controller=self, loja_info=loja_info)
            self.frames['EditarLoja'].grid(row=0, column=0, sticky="nsew")
        elif page_name == 'ListaLojasAdm':
            self.frames['ListaLojasAdm'].refresh()
        elif page_name == 'ListaLojas':
            self.frames['ListaLojas'].refresh()

        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
