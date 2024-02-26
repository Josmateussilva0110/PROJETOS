import mysql.connector 


class Armazenar_horario():
    """
    Classe para armazenar e gerenciar dados de horários.

    Attributes
    ----------
        conexao (mysql.connector.connection.MySQLConnection): A conexão com o banco de dados MySQL.

    Methods
    ----------
    drop_tabela_data(self):
        Exclui a tabela 'Data' se ela existir no banco de dados 'Agenda'.

    criar_tabela_data(self):
        Cria a tabela 'Data' no banco de dados 'Agenda' se ela não existir.

    add_data(self, data, hora):
        Adiciona uma entrada de data e hora à tabela 'Data'.

    buscar_data(self, data):
        Recupera os dados para uma data específica da tabela 'Data'.

    buscar_todas_datas(self):
        Recupera todas as datas armazenadas na tabela 'Data'.

    delete_data(self, data):
        Exclui uma entrada de data específica da tabela 'Data'.

    buscar_horarios_dia(self, dia):
        Recupera todas as entradas de horário para uma data específica da tabela 'Data'.

    delete_horario(self, horario, dia):
        Exclui uma entrada de horário específica para uma data fornecida da tabela 'Data'.
    """

    def __init__(self, conexao):
        self.conexao = conexao
        self.drop_tabela_data()
        self.criar_tabela_data()
    

    def drop_tabela_data(self):
        """
        Exclui a tabela 'Data' se ela existir no banco de dados 'Agenda'.

        Returns
        -------
        bool
            Retorna True se a tabela foi excluída com sucesso, False caso contrário.
        """

        cursor = self.conexao.cursor()
        cursor.execute("USE Agenda")
        try:
            cursor.execute("SHOW TABLES LIKE 'Data'")
            table_exists = cursor.fetchone()
            if table_exists:
                query = "DROP TABLE Data"
                cursor.execute(query)
                self.conexao.commit()
                return True
        except mysql.connector.Error as err:
            print(f"Erro ao tentar excluir a tabela Data: {err}")
            self.conexao.rollback()
            return False
        finally:
            cursor.close()

    

    def criar_tabela_data(self):
        """
        Cria a tabela 'Data' no banco de dados 'Agenda' se ela não existir.
        """

        cursor = self.conexao.cursor()
        cursor.execute("USE Agenda")
        criar_tabela = """
        CREATE TABLE IF NOT EXISTS Data(
            datas VARCHAR(255) NOT NULL,
            horas VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(criar_tabela)
        self.conexao.commit()
        cursor.close()


    def add_data(self, data, hora):
        """
        Adiciona uma entrada de data e hora à tabela 'Data'.

        Parameters
        ----------
        data : str
            A data a ser adicionada.
        hora : str
            A hora a ser adicionada.

        Returns
        -------
        bool
            Retorna True se a operação for bem-sucedida, False caso contrário.
        """

        cursor = self.conexao.cursor()
        valid = False
        query_add = "INSERT INTO Data(datas, horas) VALUES (%s, %s)"
        values = (data, hora)
        try:
            cursor.execute(query_add, values)
            self.conexao.commit()
            valid = True
            cursor.close()
        except mysql.connector.Error:
            self.conexao.rollback()
            cursor.close()
        return valid

    def buscar_data(self, data):
        """
        Recupera os dados para uma data específica da tabela 'Data'.

        Parameters
        ----------
        data : str
            A data a ser recuperada.

        Returns
        -------
        tuple or None
            Retorna uma tupla contendo os dados se a data existir, None caso contrário.
        """

        cursor = self.conexao.cursor()  
        query = "SELECT * FROM Data WHERE datas = %s"
        
        try:
            cursor.execute(query, (data,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result
            else:
                return None
        except mysql.connector.Error as err:
            print(f'Erro ao buscar data : {err}')
            cursor.close()
            return None
    
    def buscar_todas_datas(self):
        """
        Recupera todas as datas armazenadas na tabela 'Data'.

        Returns
        -------
        list or None
            Retorna uma lista de strings formatadas com as datas se houver, None caso contrário.
        """

        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT datas FROM Data")
            datas = cursor.fetchall()
            datas_strings = [f"Dia: {dia}\n" for dia in datas]
            return datas_strings
        except Exception as e:
            return None
    

    def delete_data(self, data):
        """
        Exclui uma data específica da tabela 'Data'.

        Parameters
        ----------
        data : str
            A data a ser excluída.

        Returns
        -------
        bool
            Retorna True se a operação for bem-sucedida, False caso contrário.
        """

        cursor = self.conexao.cursor()
        try:
            query = "DELETE FROM Data WHERE datas = %s"
            cursor.execute(query, (data,))
            self.conexao.commit()
            return True
        except mysql.connector.Error as err:
            print(f'Erro em deletar: {err}')
            return False
        finally:
            cursor.close()
    

    def buscar_horarios_dia(self, dia):
        """
        Recupera todos os horários para uma data específica da tabela 'Data'.

        Parameters
        ----------
        dia : str
            O dia para o qual os horários devem ser recuperados.

        Returns
        -------
        list or None
            Retorna uma lista de horários se houver, None caso contrário.
        """

        cursor = self.conexao.cursor()
        query = "SELECT * FROM Data WHERE datas = %s"
        try:
            cursor.execute(query, (dia, ))
            result = cursor.fetchone()
            if result:
                horarios = result[1]
                cursor.close()
                horarios_list = horarios.split(',')
                return horarios_list
            else:
                cursor.close()
                return None
        except mysql.connector.Error as err:
            print(f'Erro em buscar horarios: {err}')
            return False
    

    def delete_horario(self, horario, dia):
        """
        Exclui um horário específica para uma data fornecida da tabela 'Data'.

        Parameters
        ----------
        horario : str
            O horário a ser excluído.
        dia : str
            O dia para o qual o horário deve ser removido.

        Returns
        -------
        bool
            Retorna True se a operação for bem-sucedida, False caso contrário.
        """
        cursor = self.conexao.cursor()
        query = "SELECT * FROM Data WHERE datas = %s"
        try:
            cursor.execute(query, (dia, ))
            result = cursor.fetchall()
            if result:
                for row in result:
                    datas = row[0]
                    horas = row[1]
                horarios_list = horas.split(',')
                if horario in horarios_list:
                    horarios_list.remove(horario)
                update_horarios = ','.join(horarios_list)
                query_update = "UPDATE Data SET horas = %s WHERE datas = %s"
                cursor.execute(query_update, (update_horarios, datas))
                self.conexao.commit()
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f'falha em excluir horario: {err}')
            return False
        finally:
            cursor.close()
