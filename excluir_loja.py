import tkinter as tk
from conexao_bd import create_connection, delete_loja  

def excluir_loja(loja_id, frame):
    confirmacao = tk.Tk()
    confirmacao.title("Confirmação de Exclusão")

    confirmacao_frame = tk.Frame(confirmacao)
    confirmacao_frame.pack(padx=20, pady=10)

    lbl_confirmacao = tk.Label(confirmacao_frame, text="Deseja realmente excluir esta loja?")
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

    btn_confirmar = tk.Button(confirmacao_frame, text="Confirmar", command=confirmar_exclusao)
    btn_confirmar.pack(side=tk.LEFT, padx=5)

    btn_cancelar = tk.Button(confirmacao_frame, text="Cancelar", command=cancelar_exclusao)
    btn_cancelar.pack(side=tk.RIGHT, padx=5)

    confirmacao.mainloop()