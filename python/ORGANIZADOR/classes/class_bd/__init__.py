import mysql.connector

def configurar_conexao():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="12345678",
        )
        return mydb
    except mysql.connector.Error:
        return None
    
def criar_base_dados():
    mybd = configurar_conexao()
    cursor = mybd.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Agenda")
