import sys
import socket
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QInputDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt, QDate

from telas.cliente.tela_principal_cliente import *
from telas.cliente.tela_dias_disponiveis import *
from telas.cliente.tela_cadastro_cliente import *
from telas.cliente.tela_inicial import *
from telas.cliente.tela_excluir_cliente import *
from classes.funcoes_aux import *



ip = '10.0.0.44'
porta = 8008
addr = ((ip,porta))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(addr)
except Exception as e:
    print(f'Erro {e}')
    exit()


class Main(QtWidgets.QWidget):
    """
    Classe que representa a janela principal da aplicação com um layout empilhado para alternar entre diferentes telas.
    """

    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()
        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()


        self.tela_login = Tela_inicial()
        self.tela_login.setupUi(self.stack0)


        self.tela_principal = Tela_principal_cliente()
        self.tela_principal.setupUi(self.stack1)

        self.lista_dias_disponiveis = Lista_dias_disponiveis()
        self.lista_dias_disponiveis.setupUi(self.stack2)


        self.tela_cadastro_cliente = Cadastro_cliente()
        self.tela_cadastro_cliente.setupUi(self.stack3)

        self.tela_excluir_cliente = Excluir_cliente()
        self.tela_excluir_cliente.setupUi(self.stack4)


        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)


class Master(QMainWindow, Main):
    """
    Classe principal que gerencia a interface gráfica do cliente.

    Attributes
    ----------
    QtStack : PyQt5.QtWidgets.QStackedLayout
        Layout para alternar entre diferentes janelas.
    stack0 : PyQt5.QtWidgets.QMainWindow
        Janela principal da aplicação.
    stack1 : PyQt5.QtWidgets.QMainWindow
        Janela para a exibição do calendário.
    stack2 : PyQt5.QtWidgets.QMainWindow
        Janela para a seleção de horários.
    stack3 : PyQt5.QtWidgets.QMainWindow
        Janela para a exclusão de horários.
    stack4 : PyQt5.QtWidgets.QMainWindow
        Janela para a exibição de reservas dos clientes.
    nome : str
        O nome do cliente.
    cpf : str
        O CPF do cliente.
    lista_dados : list
        Lista para armazenar dados temporários.

    Methods
    -------
    sair_sistema()
        Fecha a aplicação.
    voltar_tela_login()
        Retorna à tela de login.
    voltar_tela_principal()
        Retorna à tela principal.
    tela_dias_disponiveis()
        Navega para a tela de dias disponíveis.
    voltar_tela_cadastro_cliente()
        Retorna à tela de cadastro de cliente.
    tela_excluir()
        Navega para a tela de exclusão.
    selecionar_dia(index)
        Seleciona um dia na lista de dias disponíveis.
    add_dias_disponives_listview()
        Adiciona os dias disponíveis à lista na interface gráfica.
    botao_cadastrar()
        Executa o cadastro de cliente.
    verificar_login()
        Verifica o login do cliente.
    buscar_nome_cpf(cpf)
        Busca o nome associado a um CPF no servidor.
    verificar_cpf_servidor(cpf)
        Verifica se um CPF já está cadastrado no servidor.
    enviar_pedido(lista)
        Envia um pedido de reserva ao servidor.
    atualizar_horarios(dia)
        Atualiza a lista de horários disponíveis para um dia específico.
    add_dias_listview_excluir(cpf)
        Adiciona os dias disponíveis para exclusão à lista na interface gráfica.
    selecionar_excluir(index)
        Seleciona um dia para excluir na lista de dias disponíveis.
    realizar_exclusao_dia(cpf, dia)
        Realiza a exclusão de uma reserva para um determinado dia.
    buscar_email(cpf)
        Busca o email associado a um CPF no servidor.
    """

    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)
        self.tela_login.pushButton_3.clicked.connect(self.sair_sistema)
        self.tela_login.pushButton_5.clicked.connect(self.voltar_tela_cadastro_cliente)
        self.tela_login.pushButton_4.clicked.connect(self.verificar_login)
        self.tela_principal.pushButton_3.clicked.connect(self.voltar_tela_login)
        self.tela_principal.pushButton.clicked.connect(self.tela_dias_disponiveis)
        self.tela_principal.pushButton_2.clicked.connect(self.tela_excluir)
        self.lista_dias_disponiveis.pushButton_3.clicked.connect(self.voltar_tela_principal)
        self.lista_dias_disponiveis.listView.clicked.connect(self.selecionar_dia)
        self.tela_cadastro_cliente.pushButton_3.clicked.connect(self.voltar_tela_login)
        self.tela_cadastro_cliente.pushButton_4.clicked.connect(self.botao_cadastrar)
        self.tela_excluir_cliente.pushButton_3.clicked.connect(self.voltar_tela_principal)
        self.tela_excluir_cliente.listView.clicked.connect(self.selecionar_excluir)
        self.nome = ''
        self.cpf = ''
        self.lista_dados = list()
    

    def sair_sistema(self):
        """
        Fecha a aplicação.
        """

        client_socket.send('0'.encode())
        sys.exit()
    
    def voltar_tela_login(self):
        """
        Retorna à tela de login.
        """

        self.QtStack.setCurrentIndex(0)
    
    def voltar_tela_principal(self):
        """
        Retorna à tela principal.
        """

        self.QtStack.setCurrentIndex(1)
    
    def tela_dias_disponiveis(self):
        """
        Adiciona os dias disponíveis à lista.
        """

        self.QtStack.setCurrentIndex(2)
        self.add_dias_disponives_listview()
    
    def voltar_tela_cadastro_cliente(self):
        """
        Retorna à tela de cadastro de cliente.
        """

        self.QtStack.setCurrentIndex(3)
    
    def tela_excluir(self):
        """
        Adiciona os dias disponíveis para exclusão à lista.
        """

        self.QtStack.setCurrentIndex(4)
        self.add_dias_listview_excluir(self.cpf)
    
    def selecionar_dia(self, index):
        """
        Seleciona um dia na lista de dias disponíveis.

        Parameters
        ----------
        index : QModelIndex
            O índice do item selecionado.
        """

        if index.isValid():
            item_selecionado = index.data()
            resposta = QMessageBox.question(self, 'Data', 'Deseja selecionar esse dia?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if resposta == QMessageBox.Yes:
                dia = item_selecionado[5:]
                client_socket.send('5'.encode())
                client_socket.send(str(dia).encode())
                try:
                    resposta = client_socket.recv(4096).decode()
                except:
                    QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                    client_socket.close()
                if resposta == '1':
                    horarios = client_socket.recv(4096).decode()
                    horarios_list = horarios.split(',')
                    aux = self.atualizar_horarios(dia)
                    if aux:
                        for i in aux:
                            horarios_list.remove(i)
                    if len(horarios_list) == 0:
                        QtWidgets.QMessageBox.information(self, 'Data', 'dia indisponivel, sem horarios')
                    else:
                        horario_selecionado, ok = QInputDialog.getItem(self, 'Seleção', 'Selecione o horário:', horarios_list, 0, False)
                        if ok:
                            resposta = QMessageBox.question(self, 'Data', 'Finalizar escolha?', QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
                            if resposta == QMessageBox.Yes:
                                self.lista_dados.append(self.cpf)
                                self.lista_dados.append(dia)
                                self.lista_dados.append(horario_selecionado)
                                self.lista_dados.append(self.nome)
                                self.enviar_pedido(self.lista_dados)
                            else:
                                QtWidgets.QMessageBox.information(self, 'Data', 'Escolha cancelada.')
                                self.lista_dados.clear()
                        else:
                            QtWidgets.QMessageBox.information(self, 'Data', 'Escolha cancelada.')
                            self.lista_dados.clear()

    
    def add_dias_disponives_listview(self):
        """
        Adiciona os dias disponíveis à lista no listview.
        """

        client_socket.send('3'.encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()

        if resposta == '1':
            datas = client_socket.recv(4096).decode()
            model = QStringListModel()
            info = extrair_informacoes_datas(datas)
            formatado = formatar_informacoes_data(info)
            model.setStringList(formatado)
            self.lista_dias_disponiveis.listView.setModel(model)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Não ha dia disponível.')
            self.voltar_tela_principal()
    

    def botao_cadastrar(self):
        """
        Executa o cadastro de cliente.
        """

        lista_dados = list()
        valid = False
        cpf = self.tela_cadastro_cliente.lineEdit_2.text()
        nome = self.tela_cadastro_cliente.lineEdit.text()
        email = self.tela_cadastro_cliente.lineEdit_3.text()
        if validacao(cpf, nome, email):
            if self.verificar_cpf_servidor(cpf):
                QtWidgets.QMessageBox.information(self, 'Erro', 'CPF ja cadastrado.')
            else:
                lista_dados.append(cpf)
                lista_dados.append(nome)
                lista_dados.append(email)
                enviar = ','.join(lista_dados)
                client_socket.send('6'.encode())
                client_socket.send(enviar.encode())
                try:
                    resposta = client_socket.recv(4096).decode()
                except:
                    QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                    client_socket.close()
                if resposta == '1':
                    QtWidgets.QMessageBox.information(self, 'Horario', 'Cliente armazenado com sucesso.')
                    valid = True
                else:
                    QtWidgets.QMessageBox.information(self, 'Horario', 'Falha ao cadastrar.')
                    self.voltar_tela_principal()
        else:
            QtWidgets.QMessageBox.information(self, 'Dados', 'Dados inválidos.')
        self.tela_cadastro_cliente.lineEdit_2.clear()
        self.tela_cadastro_cliente.lineEdit.clear()
        self.tela_cadastro_cliente.lineEdit_3.clear()
        if valid:
            self.QtStack.setCurrentIndex(0)
    

    def verificar_login(self):
        """
        Verifica o login do cliente.
        """

        cpf = self.tela_login.lineEdit_2.text()
        if not verificar_valor_inteiro(cpf) or cpf == '':
            QtWidgets.QMessageBox.information(self, 'Login', 'Digite valores validos.')
        else:
            client_socket.send('8'.encode())
            client_socket.send(cpf.encode())
            try:
                resposta = client_socket.recv(4096).decode()
            except:
                QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                client_socket.close()
            if resposta == '1':
                QtWidgets.QMessageBox.information(self, 'Login', 'Login realizado com sucesso.')
                self.cpf = cpf
                nome = self.buscar_nome_cpf(cpf)
                if nome != None:
                    self.tela_principal.label_4.setText(nome)
                    self.nome = nome
                self.voltar_tela_principal()
            else:
                QtWidgets.QMessageBox.information(self, 'Login', 'Falha com o login.')
        self.tela_login.lineEdit_2.clear()
    

    def buscar_nome_cpf(self, cpf):
        """
        Busca o nome associado a um CPF no servidor.

        Parameters
        ----------
        cpf : str
            O CPF do cliente.

        Returns
        -------
        str or None
            Retorna o nome associado ao CPF se encontrado, None caso contrário.
        """

        client_socket.send('9'.encode())
        client_socket.send(str(cpf).encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            nome = client_socket.recv(4096).decode()
            return nome
        else:
            return None
    
    def verificar_cpf_servidor(self, cpf):
        """
        Verifica se um CPF já está cadastrado no servidor.

        Parameters
        ----------
        cpf : str
            O CPF a ser verificado.

        Returns
        -------
        bool
            Retorna True se o CPF já estiver cadastrado, False caso contrário.
        """

        client_socket.send('8'.encode())
        client_socket.send(str(cpf).encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            return True
        else:
            return False
        
    
    def enviar_pedido(self, lista):
        """
        Envia um pedido de reserva ao servidor.

        Parameters
        ----------
        lista : list
            Lista contendo informações do pedido.
        """

        enviar = ','.join(lista)
        client_socket.send('10'.encode())
        client_socket.send(enviar.encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            QtWidgets.QMessageBox.information(self, 'Reserva', 'Reserva cadastrada com sucesso.')
            msg = formatar_mensagem(lista[3], lista[1], lista[2])
            email = self.buscar_email(self.cpf)
            if email != 0:
                EnviaEmail(email, msg)
                QtWidgets.QMessageBox.information(self, 'Reserva', 'Comprovante enviado por email')
            self.voltar_tela_principal()
            self.lista_dados.clear()
        else:
            QtWidgets.QMessageBox.information(self, 'Reserva', 'Erro ao salvar dados.')
    

    def atualizar_horarios(self, dia):
        """
        Atualiza a lista de horários disponíveis para um dia específico.

        Parameters
        ----------
        dia : str
            O dia para o qual se deseja obter os horários disponíveis.

        Returns
        -------
        list
            Retorna a lista de horários já reservados para o dia.
        """

        client_socket.send('11'.encode())
        client_socket.send(str(dia).encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            horarios = client_socket.recv(4096).decode()
            horarios_list = horarios.split(',')
            return horarios_list
    

    def add_dias_listview_excluir(self, cpf):
        """
        Adiciona os dias disponíveis para exclusão à lista na interface gráfica.

        Parameters
        ----------
        cpf : str
            O CPF do cliente para o qual se deseja obter os dias disponíveis.
        """

        client_socket.send('12'.encode())
        client_socket.send(str(cpf).encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()

        if resposta == '1':
            datas = client_socket.recv(4096).decode()
            model = QStringListModel()
            info = extrair_informacoes_datas(datas)
            formatado = formatar_informacoes_data(info)
            model.setStringList(formatado)
            self.tela_excluir_cliente.listView.setModel(model)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Não ha dia disponível.')
            self.voltar_tela_principal()
    

    def selecionar_excluir(self, index):
        """
        Seleciona um dia para excluir na lista de dias disponíveis.

        Parameters
        ----------
        index : QModelIndex
            O índice do item selecionado.
        """

        item_selecionado = index.data()
        dia = item_selecionado[5:16]
        resposta = QMessageBox.question(self, 'Data', 'Deseja excluir esse dia?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.realizar_exclusao_dia(self.cpf,dia)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Operação cancelada.')
    

    def realizar_exclusao_dia(self, cpf, dia):
        """
        Realiza a exclusão de uma reserva para um determinado dia.

        Parameters
        ----------
        cpf : str
            O CPF do cliente.
        dia : str
            O dia da reserva a ser excluída.
        """

        lista = list()
        lista.append(cpf)
        lista.append(dia)
        enviar = ','.join(lista)
        client_socket.send('13'.encode())
        client_socket.send(enviar.encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            QtWidgets.QMessageBox.information(self, 'Data', 'reserva excluida com sucesso.')
            self.QtStack.setCurrentIndex(1)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Erro ao excluir a reserva.')
    

    def buscar_email(self, cpf):
        """
        Busca o email associado a um CPF no servidor.

        Parameters
        ----------
        cpf : str
            O CPF do cliente.

        Returns
        -------
        str or 0
            Retorna o email associado ao CPF se encontrado, 0 caso contrário.
        """

        client_socket.send('17'.encode())
        client_socket.send(str(cpf).encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            email = client_socket.recv(4096).decode()
            return email
        else:
            return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Master()
    sys.exit(app.exec_())
