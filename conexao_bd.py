import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='lojas',
            user='root',
            password='12345'
        )
        if connection.is_connected():
            print("Conexão ao MySQL estabelecida com sucesso")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def add_loja(connection, nome, descricao, media_preco, url_img, rua, bairro, numero_endereco):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO lojas (nome, descricao, media_preco, url_img, rua, bairro, numero_endereco) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (nome, descricao, media_preco, url_img, rua, bairro, numero_endereco)
        cursor.execute(query, values)
        connection.commit()
        print("Loja adicionada com sucesso")
    except Error as e:
        print(f"Erro ao adicionar loja: {e}")

def update_loja(connection, loja_id, nome=None, descricao=None, media_preco=None, url_img=None, rua=None, bairro=None, numero_endereco=None):
    try:
        cursor = connection.cursor()
        query = "UPDATE lojas SET "
        fields = []
        values = []

        if nome:
            fields.append("nome = %s")
            values.append(nome)
        if descricao:
            fields.append("descricao = %s")
            values.append(descricao)
        if media_preco:
            fields.append("media_preco = %s")
            values.append(media_preco)
        if url_img:
            fields.append("url_img = %s")
            values.append(url_img)
        if rua:
            fields.append("rua = %s")
            values.append(rua)
        if bairro:
            fields.append("bairro = %s")
            values.append(bairro)
        if numero_endereco:
            fields.append("numero_endereco = %s")
            values.append(numero_endereco)

        query += ", ".join(fields)
        query += " WHERE id = %s"
        values.append(loja_id)

        cursor.execute(query, values)
        connection.commit()
        print("Loja atualizada com sucesso")
    except Error as e:
        print(f"Erro ao atualizar loja: {e}")

def delete_loja(connection, id_loja):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM lojas WHERE id = %s"
        cursor.execute(query, (id_loja,))
        connection.commit()
        print("Loja removida com sucesso")
    except Error as e:
        print(f"Erro ao remover loja: {e}")

def read_lojas(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM lojas"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Erro ao ler lojas: {e}")
        return None