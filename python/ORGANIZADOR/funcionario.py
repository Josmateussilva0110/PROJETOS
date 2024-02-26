import sys
import socket
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QCalendarWidget, QMessageBox, QInputDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt, QDate


from telas.gerente.calendario import *
from telas.gerente.selecao_horario import *
from telas.gerente.tela_principal import *
from telas.gerente.excluir_horarios import *
from telas.gerente.reserva_clientes import *
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
        """
        Configura a interface do usuário para a janela principal da aplicação, incluindo várias telas empilhadas.
        """

        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()
        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()


        self.tela_principal = Tela_principal()
        self.tela_principal.setupUi(self.stack0)

        self.calendario = Calendario()
        self.calendario.setupUi(self.stack1)

        self.selecao_horario = Selecao_horario()
        self.selecao_horario.setupUi(self.stack2)

        self.excluir_horario = Excluir_horarios()
        self.excluir_horario.setupUi(self.stack3)


        self.reserva_cliente = Reserva_clientes()
        self.reserva_cliente.setupUi(self.stack4)


        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)


class Master(QMainWindow, Main):
    """
    Classe principal que controla a interface gráfica e interação do usuário.

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

    Methods
    -------
    pegar_data(selected_date)
        Obtém a data selecionada pelo usuário no calendário.

    selecionar_horarios()
        Adiciona o horário selecionado à lista de horários.

    add_hora_listview()
        Adiciona os horários selecionados.

    botao_cadastra()
        Cadastrar os horários escolhidos.

    add_datas_listview_excluir()
        Adiciona as datas disponíveis para exclusão.

    selecionar_excluir(index)
        Executa a ação de excluir horário ou data, conforme a seleção.

    fechar_aplicacao()
        Fecha a aplicação.

    voltar_tela_principal()
        Retorna à tela principal.

    tela_calendario()
        Exibe a tela de seleção de datas/calendário.

    tela_excluir_horario()
        Exibe a tela de exclusão de horários.

    retornar_horarios(dia)
        Retorna os horários disponíveis para um determinado dia.

    realizar_exclusao_horario(dia)
        Executa a exclusão de um horário específico.

    realizar_exclusao_dia(dia)
        Executa a exclusão de todos os horários de um dia.

    ver_reservas()
        Exibe a tela com a lista de reservas dos clientes.

    delete_all()
        Executa a exclusão de todos os horários e datas.

    verificar_pedidos_cadastrados()
        Verifica se há pedidos cadastrados.
    """

    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)
        self.calendario.pushButton.clicked.connect(self.voltar_tela_principal)
        self.calendario.calendarWidget.clicked.connect(self.pegar_data)
        self.selecao_horario.pushButton_2.clicked.connect(self.tela_calendario)
        self.selecao_horario.pushButton.clicked.connect(self.selecionar_horarios)
        self.selecao_horario.pushButton_3.clicked.connect(self.botao_cadastra)
        self.tela_principal.pushButton_3.clicked.connect(self.fechar_aplicacao)
        self.tela_principal.pushButton.clicked.connect(self.tela_calendario)
        self.tela_principal.pushButton_2.clicked.connect(self.tela_excluir_horario)
        self.tela_principal.pushButton_4.clicked.connect(self.ver_reservas)
        self.excluir_horario.pushButton_2.clicked.connect(self.voltar_tela_principal)
        self.excluir_horario.listView.clicked.connect(self.selecionar_excluir)
        self.excluir_horario.pushButton_3.clicked.connect(self.delete_all)
        self.reserva_cliente.pushButton_2.clicked.connect(self.voltar_tela_principal)
        self.datas = dict()
        self.horarios_selecionados = list()
        self.data = ''


    def pegar_data(self, selected_date):
        """
        Captura a data selecionada e processa a escolha.

        Parameters
        ----------
        selected_date : QDate
            A data selecionada no calendário.
        """  

        resposta = QMessageBox.question(self, 'Data', 'Finalizar escolha?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
        if resposta == QMessageBox.Yes:
            formatted_date = selected_date.toString('MMM dd yyyy')
            str_date = str(formatted_date)
            print(f'{str_date}')
            date_str = str_date
            self.data = date_str
            first = self.data[4:6]
            mid = self.data[:3]
            end = self.data[7:]
            tran = '/'
            new = first + tran + mid + tran + end
            client_socket.send('2'.encode())
            client_socket.send(new.encode())
            try:
                resposta = client_socket.recv(4096).decode()
            except:
                QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                client_socket.close()
            if resposta == '0':
                QtWidgets.QMessageBox.information(self, 'Data', 'Dia já escolhido.')
            else:
                self.QtStack.setCurrentIndex(2) 
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Nenhuma data selecionada.')


    def selecionar_horarios(self):
        """
        Captura o horário selecionado e o adiciona à lista de horários selecionados.
        """

        hora_str = self.selecao_horario.timeEdit.time().toString("HH:mm")
        self.horarios_selecionados.append(hora_str)
        self.add_hora_listview()
    
    def add_hora_listview(self):
        """
        Adiciona os horários selecionados à listView na interface gráfica.
        """

        if self.horarios_selecionados:
            horario_usar = self.selecao_horario.listView
            modelo_horario = QStandardItemModel()
            for hora in self.horarios_selecionados:
                item_horario = QStandardItem(hora)
                item_horario.setEditable(False)
                modelo_horario.appendRow(item_horario)
            horario_usar.setModel(modelo_horario)
        else:
            QtWidgets.QMessageBox.information(self, 'Horário', 'Selecione um horário antes de adicionar.')
    

    def botao_cadastra(self):
        """
        Realiza o cadastro dos horários selecionados para a data escolhida.
        """

        if len(self.horarios_selecionados) == 0:
            QtWidgets.QMessageBox.information(self, 'Dados', 'Selecione um horario.')
            self.QtStack.setCurrentIndex(2)
        else:
            lista_dados = list()
            first = self.data[4:6]
            mid = self.data[:3]
            end = self.data[7:]
            tran = '/'
            new = first + tran + mid + tran + end
            lista_dados.append(new)
            v = ','.join(self.horarios_selecionados)
            lista_dados.append(v)
            enviar = ','.join(lista_dados)
            client_socket.send('1'.encode())
            client_socket.send(enviar.encode())
            try:
                resposta = client_socket.recv(4096).decode()
            except:
                QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                client_socket.close()
            if resposta == '1':
                QtWidgets.QMessageBox.information(self, 'Dados', 'Dados salvo com sucesso.')
            elif resposta == '2':
                QtWidgets.QMessageBox.information(self, 'Dados', 'Dia já escolhido.')
            else:
                QtWidgets.QMessageBox.information(self, 'Dados', 'Erro ao salvar os dados.')
            self.QtStack.setCurrentIndex(0)
        self.horarios_selecionados.clear()
        self.selecao_horario.listView.setModel(QStandardItemModel())
        self.selecao_horario.listView.setModel(QStandardItemModel())
        self.selecao_horario.timeEdit.setTime(QtCore.QTime(0, 0, 0))


    def add_datas_listview_excluir(self):
        """
        Atualiza a listView na interface gráfica com as datas disponíveis para exclusão.
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
            self.excluir_horario.listView.setModel(model)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Nenhuma data encontrada.')
            self.voltar_tela_principal()
    

    def selecionar_excluir(self, index):
        """
        Captura a seleção do usuário para excluir horários ou datas.

        Parameters
        ----------
        index : QModelIndex
            O índice selecionado na listView.
        """

        if index.isValid():
            item_selecionado = index.data()
            dia = item_selecionado[5:]
            resposta = QMessageBox.question(self, 'Data', 'Deseja excluir algum horario?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if resposta == QMessageBox.No:
                resposta = QMessageBox.question(self, 'Data', 'Deseja excluir essa data?', QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
                if resposta == QMessageBox.Yes:
                    self.realizar_exclusao_dia(dia)
                else:
                    QtWidgets.QMessageBox.information(self, 'Data', 'Operação cancelada.')
            else:
                self.realizar_exclusao_horario(dia)


    def fechar_aplicacao(self):
        """
        Fecha a aplicação e encerra a conexão com o servidor.
        """

        client_socket.send('0'.encode())
        sys.exit()

    def voltar_tela_principal(self):
        """
        Volta para a tela principal, limpando as seleções de horários.
        """

        self.horarios_selecionados.clear()
        self.QtStack.setCurrentIndex(0) 

    def tela_calendario(self):
        """
        Navega para a tela do calendário, limpando as seleções de horários.
        """

        self.horarios_selecionados.clear()
        self.QtStack.setCurrentIndex(1)

    
    def tela_excluir_horario(self):
        """
        Navega para a tela de exclusão de horários, atualizando as datas disponíveis.
        """

        self.QtStack.setCurrentIndex(3)
        self.add_datas_listview_excluir()
    

    def retornar_horarios(self, dia):
        """
        Retorna os horários disponíveis para um determinado dia.

        Parameters
        ----------
        dia : str
            A data para a qual os horários serão consultados.

        Returns
        -------
        List or None
            Lista de horários disponíveis ou None se nenhum horário estiver disponível.
        """

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
            return horarios_list
        else:
            return None
        

    def realizar_exclusao_horario(self, dia):
        """
        Realiza a exclusão de um horário para uma determinada data.

        Parameters
        ----------
        dia : str
            A data para a qual o horário será excluído.
        """

        horarios_list = self.retornar_horarios(dia)
        if len(horarios_list) == 1:
            resposta = QMessageBox.question(self, 'Data', 'A operação ira excluir o dia, deseja continuar operação?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.realizar_exclusao_dia(dia)
                return
            else:
                return
        if horarios_list:
            horario_selecionado, ok = QInputDialog.getItem(self, 'Seleção', 'Selecione o horário:', horarios_list, 0, False)
            if ok:
                lista = list()
                lista.append(horario_selecionado)
                lista.append(dia)
                enviar = ','.join(lista)
                client_socket.send('7'.encode())
                client_socket.send(enviar.encode())
                try:
                    resposta = client_socket.recv(4096).decode()
                except:
                    QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                    client_socket.close()
                if resposta == '1':
                    QtWidgets.QMessageBox.information(self, 'Excluir', 'Horario excluido com sucesso.')
                    self.voltar_tela_principal()
                else:
                    QtWidgets.QMessageBox.information(self, 'Excluir', 'Falha ao excluir o horario.')

    
    def realizar_exclusao_dia(self, dia):
        """
        Realiza a exclusão de todos os horários para uma determinada data.

        Parameters
        ----------
        dia : str
            A data para a qual todos os horários serão excluídos.
        """

        client_socket.send('4'.encode())
        client_socket.send(str(dia).encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            QtWidgets.QMessageBox.information(self, 'Data', 'Data excluida com sucesso.')
            self.QtStack.setCurrentIndex(0)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Erro ao excluir a data.')
    

    def ver_reservas(self):
        """
        Exibe as reservas existentes na interface gráfica.
        """

        client_socket.send('14'.encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        if resposta == '1':
            dados = client_socket.recv(4096).decode()
            lista_dados = dados.split('\n')
            model = QStringListModel()
            model.setStringList(lista_dados)
            self.reserva_cliente.listView.setModel(model)
            
            self.QtStack.setCurrentIndex(4)
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'Nenhuma dado encontrada.')
            self.voltar_tela_principal()
    

    def delete_all(self):
        """
        Exclui todas as datas e horários disponíveis.
        """

        ans = self.verificar_pedidos_cadastrados()
        if int(ans) == 0:
            resposta = QMessageBox.question(self, 'Data', 'A operação ira excluir todas as datas, deseja continuar operação?', QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            if resposta == QMessageBox.Yes:
                client_socket.send('15'.encode())
                try:
                    resposta = client_socket.recv(4096).decode()
                except:
                    QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
                    client_socket.close()
                if resposta == '1':
                    QtWidgets.QMessageBox.information(self, 'Data', 'Datas apagadas com sucesso.')
                    self.voltar_tela_principal()
            else:
                QtWidgets.QMessageBox.information(self, 'Data', 'Operação cancelada.')
        else:
            QtWidgets.QMessageBox.information(self, 'Data', 'A ação não pode ser realizada pois um cliente já selecionou um horario.')
    

    def verificar_pedidos_cadastrados(self):
        """
        Verifica se existem pedidos cadastrados.

        Returns
        -------
        str
            Retorna '0' se não houver pedidos, '1' se houver pelo menos um pedido cadastrado.
        """

        client_socket.send('16'.encode())
        try:
            resposta = client_socket.recv(4096).decode()
        except:
            QtWidgets.QMessageBox.information(self, 'Data', 'Falha com o servidor.')
            client_socket.close()
        return resposta



if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Master()
    sys.exit(app.exec_())
