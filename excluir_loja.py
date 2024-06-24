import tkinter as tk
from tkinter import font as tkfont
from conexao_bd_lojas import create_connection, delete_loja  

def excluir_loja(loja_id, frame):
    confirmacao = tk.Tk()
    confirmacao.title("Confirmação de Exclusão")
    confirmacao.configure(bg="#2c3e50")
    custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
    title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

    confirmacao_frame = tk.Frame(confirmacao, bg="#2c3e50")
    confirmacao_frame.pack(padx=20, pady=10)

    lbl_confirmacao = tk.Label(confirmacao_frame, text="Deseja realmente excluir esta loja?", font=custom_font, fg="white", bg="#2c3e50")
    lbl_confirmacao.pack(pady=10)

    def confirmar_exclusao():
        connection = create_connection()

        if connection is None:
            return

        delete_loja(connection, loja_id)
        connection.close()

        print(f"Excluindo loja com ID {loja_id}")
        confirmacao.destroy()
        frame.destroy()

    def cancelar_exclusao():
        confirmacao.destroy()

    btn_confirmar = tk.Button(confirmacao_frame, text="Confirmar", command=confirmar_exclusao, font=custom_font, bg="#e74c3c", fg="white")
    btn_confirmar.pack(side=tk.LEFT, padx=5)

    btn_cancelar = tk.Button(confirmacao_frame, text="Cancelar", command=cancelar_exclusao, font=custom_font, bg="#3498db", fg="white")
    btn_cancelar.pack(side=tk.RIGHT, padx=5)

    confirmacao.mainloop()
