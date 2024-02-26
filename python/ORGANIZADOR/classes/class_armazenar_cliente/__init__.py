import mysql.connector


class Armazenar_cliente():
    """
    Classe para armazenar clientes e gerenciar dados de clientes.

    Attributes
    ----------
    conexao : mysql.connector.connection.MySQLConnection
        A conexão com o banco de dados MySQL.
    
    Methods
    -------
    drop_tabela_cliente(self)
        Exclui a tabela 'Cliente' se ela existir no banco de dados 'Agenda'.
    
    def criar_tabela_cliente(self)
        Cria a tabela 'Cliente' se ela não existir no banco de dados.
    
    def add_cliente(self, lista)
        Adiciona um cliente na tabela 'Cliente'.

    buscar_cpf(self, cpf)
        Procura um CPF em especifico na tabela 'cliente'.
    
    buscar_nome(self, cpf)
        Recupera o nome do CPF em especifico na tabela 'Cliente'.
    
    buscar_email_cpf(self, cpf)
        Recupera o e-mail de um CPF em especifico da tabela 'Cliente'.
    """

    def __init__(self, conexao):
        self.conexao = conexao
        self.drop_tabela_cliente()
        self.criar_tabela_cliente()

    def drop_tabela_cliente(self):
        """
        Exclui a tabela 'Cliente' se ela existir no banco de dados 'Agenda'.
        """

        cursor = self.conexao.cursor()
        cursor.execute("USE Agenda")
        try:
            cursor.execute("SHOW TABLES LIKE 'Cliente'")
            table_exists = cursor.fetchone()
            if table_exists:
                query = "DROP TABLE Cliente"
                cursor.execute(query)
                self.conexao.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao tentar excluir a tabela Pedido: {err}")
            self.conexao.rollback()
        finally:
            cursor.close()
    

    def criar_tabela_cliente(self):
        """
        Cria a tabela 'Cliente' se ela não existir no banco de dados.
        """

        cursor = self.conexao.cursor()
        cursor.execute("USE Agenda")
        criar_tabela = """
        CREATE TABLE IF NOT EXISTS Cliente(
            cpf INT NOT NULL,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(criar_tabela)
        self.conexao.commit()
        cursor.close()
    

    def add_cliente(self, lista):
        """
        Adiciona um cliente na tabela 'Cliente'.
        
        Parameters
        ----------
        lista : list
            Lista contendo informações do cliente (CPF, nome, email).

        Returns
        -------
        bool
            Retorna True se a operação for bem-sucedida, False caso contrário.
        """

        cursor = self.conexao.cursor()
        valid = False
        query = "INSERT INTO Cliente(cpf, nome, email) VALUES (%s, %s, %s)"
        values = (int(lista[0]), lista[1], lista[2])
        try:
            cursor.execute(query, values)
            self.conexao.commit()
            valid = True
            cursor.close()
        except mysql.connector.Error as err:
            print(f'falha ao armazenar cliente: {err}')
            self.conexao.rollback()
            cursor.close()
        return valid


    def buscar_cpf(self, cpf):
        """
        Procura um CPF em especifico na tabela 'cliente'.

        Parameters
        ----------
        cpf : int
            O CPF a ser verificado.

        Returns
        -------
        bool
            Retorna True se o CPF estiver cadastrado, False caso contrário.
        """

        cursor = self.conexao.cursor()
        query = "SELECT cpf FROM Cliente WHERE cpf = %s"
        try:
            cursor.execute(query, (cpf, ))
            result = cursor.fetchone()
            if result:
                cursor.close()
                return True
        except:
            cursor.close()
            return False
        
    
    def buscar_nome(self, cpf):
        """
        Recupera o nome do CPF em especifico na tabela 'Cliente'.

        Parameters
        ----------
        cpf : int
            O CPF do cliente.

        Returns
        -------
        str or None
            Retorna o nome do cliente se encontrado, None caso contrário.
        """

        cursor = self.conexao.cursor()
        query = "SELECT nome FROM Cliente WHERE cpf = %s"
        try:
            cursor.execute(query, (cpf, ))
            result = cursor.fetchone()
            if result:
                nome = result[0]  
                nome_str = str(nome) 
                return nome_str
        except Exception as e:
            print(f"Erro na consulta de nome: {e}")
        finally:
            cursor.close()
        return None


    def buscar_email_cpf(self, cpf):
        """
        Recupera o e-mail de um CPF em especifico da tabela 'Cliente'.
        
        Parameters
        ----------
        cpf : int
            O CPF do cliente.

        Returns
        -------
        str or None
            Retorna o e-mail do cliente se encontrado, None caso contrário.
        """
        
        cursor = self.conexao.cursor()
        query = "SELECT email FROM Cliente WHERE cpf = %s"
        try:
            cursor.execute(query, (cpf, ))
            result = cursor.fetchone()
            if result:
                cursor.close()
                return result[0]
            else:
                cursor.close()
                return None

        except Exception as e:
            print(f'erro ao buscar email: {e}')
        finally:
            cursor.close()
