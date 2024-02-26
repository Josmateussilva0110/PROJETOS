from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate
import sys
from telas.calendario import *

class MinhaApp(QMainWindow, Calendario):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar o botão à função que seleciona a data
        self.pushButton.clicked.connect(self.selecionar_data)

    def selecionar_data(self):
        # Obter a data atualmente selecionada no QCalendarWidget
        data_selecionada = self.calendarWidget.selectedDate()

        # Obter a representação formatada da data
        data_formatada = data_selecionada.toString('MMM dd yyyy')

        # Imprimir a data selecionada (apenas para fins de demonstração)
        print("Data selecionada:", data_formatada)

        # Se você quiser definir uma data específica, pode fazer algo assim:
        # nova_data = QDate(2024, 2, 15)  # Substitua pelos valores desejados
        # self.calendarWidget.setSelectedDate(nova_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MinhaApp()
    mainWindow.show()
    sys.exit(app.exec_())
