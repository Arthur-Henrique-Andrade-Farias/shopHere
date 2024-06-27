import hashlib
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='lojas',
            user='root',
            password=''
        )
        if connection.is_connected():
            print("Conexão ao MySQL estabelecida com sucesso")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def cadastrar_user(connection, nome, email, senha):
    try:
        cursor = connection.cursor()
        hashed_senha = hashlib.sha256(senha.encode()).hexdigest()
        query = """INSERT INTO usuarios (nome, email, senha, isAdmin) 
                   VALUES (%s, %s, %s, %s)"""
        values = (nome, email, hashed_senha, 0)
        cursor.execute(query, values)
        connection.commit()
        
        print(f"Cadastroi realizado!")

        return True
    except Error as e:
        return False

def verificar_login(connection, email, senha):
    try:
        cursor = connection.cursor()
        hashed_senha = hashlib.sha256(senha.encode()).hexdigest()
        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, hashed_senha))
        usuario = cursor.fetchone()

        if usuario:
            return usuario
        else:
            print("Usuário não encontrado ou Login inválido")
            return None
    except Error as e:
        print(f"Erro ao obter usuário: {e}")
        return None