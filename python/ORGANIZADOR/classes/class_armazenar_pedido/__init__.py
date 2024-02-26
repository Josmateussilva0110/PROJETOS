import mysql.connector


class Armazenar_pedido():
    """
    Classe para armazenar e gerenciar dados de pedidos.

    Attributes
    ----------
    conexao : mysql.connector.connection.MySQLConnection
        A conexão com o banco de dados MySQL.

    Methods
    -------
    drop_tabela_pedido()
        Exclui a tabela 'Pedido' se ela existir no banco de dados 'Agenda'.

    criar_tabela_pedido()
        Cria a tabela 'Pedido' no banco de dados 'Agenda' se ela não existir.

    add_pedido(lista)
        Adiciona um pedido à tabela 'Pedido'.

    buscar_todos_horarios(dia)
        Recupera todos os horários reservados para um determinado dia da tabela 'Pedido'.

    delete_reserva(cpf, dia)
        Exclui uma reserva específica para um cliente em um dia específico da tabela 'Pedido'.

    buscar_todas_datas_cliente(cpf)
        Recupera todas as datas e horários reservados por um cliente específico da tabela 'Pedido'.

    buscar_todos_dados()
        Recupera todas as informações armazenadas na tabela 'Pedido'.

    contar_pedidos_cadastrados()
        Conta o número total de pedidos cadastrados na tabela 'Pedido'.

    """
        
    def __init__(self, conexao):
        self.conexao = conexao
        self.drop_tabela_pedido()
        self.criar_tabela_pedido()

    def drop_tabela_pedido(self):
        """
        Exclui a tabela 'Pedido' se ela existir no banco de dados 'Agenda'.
        """

        cursor = self.conexao.cursor()
        cursor.execute("USE Agenda")
        try:
            cursor.execute("SHOW TABLES LIKE 'Pedido'")
            table_exists = cursor.fetchone()
            if table_exists:
                query = "DROP TABLE Pedido"
                cursor.execute(query)
                self.conexao.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao tentar excluir a tabela Pedido: {err}")
            self.conexao.rollback()
        finally:
            cursor.close() 
    
    
    def criar_tabela_pedido(self):
        """
        Cria a tabela 'Pedido' no banco de dados 'Agenda' se ela não existir.
        """

        cursor = self.conexao.cursor()
        cursor.execute("USE Agenda")
        criar_tabela = """
        CREATE TABLE IF NOT EXISTS Pedido(
            cpf INT NOT NULL,
            dia VARCHAR(255) NOT NULL,
            horario VARCHAR(255) NOT NULL,
            nome VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(criar_tabela)
        self.conexao.commit()
        cursor.close()



    def add_pedido(self, lista):
        """
        Adiciona um pedido à tabela 'Pedido'.

        Parameters
        ----------
        lista : list
            Lista contendo informações do pedido (CPF, dia, horário, nome).

        Returns
        -------
        bool
            Retorna True se a operação for bem-sucedida, False caso contrário.
        """

        cursor = self.conexao.cursor()
        valid = False
        query = "INSERT INTO Pedido(cpf, dia, horario, nome) VALUES (%s, %s, %s, %s)"
        values = (int(lista[0]), lista[1], lista[2], lista[3])
        try:
            cursor.execute(query, values)
            self.conexao.commit()
            valid = True
            cursor.close()
        except mysql.connector.Error as err:
            print(f'falha ao armazenar pedido: {err}')
            self.conexao.rollback()
            cursor.close()
        return valid


    def buscar_todos_horarios(self, dia):
        """
        Recupera todos os horários reservados para um determinado dia da tabela 'Pedido'.

        Parameters
        ----------
        dia : str
            O dia para o qual os horários devem ser recuperados.

        Returns
        -------
        list
            Lista de horários reservados para o dia especificado.
        """

        cursor = self.conexao.cursor()
        query = "SELECT horario FROM Pedido WHERE dia = %s"
        try:
            cursor.execute(query, (dia,))
            result = cursor.fetchall()
            cursor.close()
            if result:
                horarios_list = [horario[0] for horario in result]
                return horarios_list
            else:
                return [] 
        except mysql.connector.Error as err:
            print(f'Erro em buscar horarios: {err}')
            return False


    def delete_reserva(self, cpf, dia):
        """
        Exclui uma reserva específica para um cliente em um dia específico da tabela 'Pedido'.

        Parameters
        ----------
        cpf : int
            O CPF do cliente.
        dia : str
            O dia da reserva a ser excluída.

        Returns
        -------
        bool
            Retorna True se a operação for bem-sucedida, False caso contrário.
        """

        cursor = self.conexao.cursor()
        query = "DELETE FROM Pedido WHERE dia = %s AND cpf = %s"
        try:
            cursor.execute(query, (dia, cpf))
            self.conexao.commit()
            return True
        except mysql.connector.Error as err:
            print(f'Erro em deletar: {err}')
            return False
        finally:
            cursor.close()
    

    def buscar_todas_datas_cliente(self, cpf):
        """
        Recupera todas as datas e horários reservados por um cliente específico da tabela 'Pedido'.

        Parameters
        ----------
        cpf : int
            O CPF do cliente.

        Returns
        -------
        list
            Lista de strings formatadas com as datas e horários reservados pelo cliente.
        """
        cursor = self.conexao.cursor()
        query = "SELECT dia, horario FROM Pedido WHERE cpf = %s"
        try:
            cursor.execute(query, (cpf, ))
            datas = cursor.fetchall()
            datas_strings = [f"Dia: {dia} - Horario: {horario}\n" for dia, horario in datas]
            return datas_strings
        except Exception as e:
            return None


    def buscar_todos_dados(self):
        """
        Recupera todas as informações armazenadas na tabela 'Pedido'.

        Returns
        -------
        list
            Lista de strings formatadas com todas as informações dos pedidos.
        """

        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Pedido")
            gerentes = cursor.fetchall()
            dados_str = [
                f"DIA: {dado[1]} - HORARIO: {dado[2]} - NOME: {dado[3]}\n"
                for dado in gerentes
            ]
            return dados_str
        except mysql.connector.Error as err:
            print(f'erro na busca dados clientes: {err}')
            return []


    def contar_pedidos_cadastrados(self):
        """
        Conta o número total de pedidos cadastrados na tabela 'Pedido'.

        Returns
        -------
        int
            Número total de pedidos cadastrados.
        """
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute("USE Agenda")
            count_query = "SELECT COUNT(*) FROM Pedido"
            cursor.execute(count_query)
            result = cursor.fetchone()
            self.conexao.commit()
            return result[0] if result else 0
        except mysql.connector.Error as err:
            print(f"Erro ao contar pessoas cadastradas: {err}")
        finally:
            cursor.close()
