import threading
import socket
from classes.class_bd import *
from classes.class_armazenar_horario import *
from classes.class_armazenar_pedido import *
from classes.class_armazenar_cliente import *

host = ''
porta = 8008
addr = (host, porta)

bd = configurar_conexao()
criar_base_dados()

h = Armazenar_horario(bd)
pedido = Armazenar_pedido(bd)
cli = Armazenar_cliente(bd)


def menu(con, cliente):
    conected = True
    while conected:
        mensagem = con.recv(4096).decode()
        if mensagem == '0':
            conected = False


        elif mensagem == '1':
            dados = con.recv(4096).decode()
            partes = dados.split(",")
            dia = partes[0]
            horarios = partes[1:]
            str_horarios = ','.join(horarios)
            buscar = h.buscar_data(dia)
            if buscar is None:
                if h.add_data(dia, str_horarios):
                    con.send('1'.encode())
                else:
                    con.send('0'.encode())
            else:
                con.send('2'.encode())

        elif mensagem == '2':
            dia = con.recv(4096).decode()
            buscar = h.buscar_data(dia)
            if buscar is None:
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '3':
            datas = h.buscar_todas_datas()
            if datas:
                elementos = [data.replace('(', '').replace(')', '').replace(',', '') for data in datas]
                datas_str = ''.join(elementos)
                con.send('1'.encode())
                con.send(datas_str.encode())
            else:
                con.send('0'.encode())
        
        elif mensagem == '4':
            data = con.recv(4096).decode()
            if h.delete_data(data):
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '5':
            dia = con.recv(4096).decode()
            aux = h.buscar_horarios_dia(dia)
            if aux:
                enviar = ','.join(aux)
                con.send('1'.encode())
                con.send(enviar.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '6':
            dados = con.recv(4096).decode()
            partes = dados.split(',')
            if cli.add_cliente(partes):
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '7':
            dados = con.recv(4096).decode()
            partes = dados.split(',')
            horario = partes[0]
            dia = partes[1]
            if h.delete_horario(horario, dia):
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '8':
            cpf = con.recv(4096).decode()
            if cli.buscar_cpf(cpf):
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        
        elif mensagem == '9':
            cpf = con.recv(4096).decode()
            aux = cli.buscar_nome(int(cpf))
            if aux:
                con.send('1'.encode())
                con.send(aux.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '10':
            dados = con.recv(4096).decode()
            partes = dados.split(',')
            if pedido.add_pedido(partes):
                con.send('1'.encode())
            else:
                con.send('0'.encode())


        elif mensagem == '11':
            dia = con.recv(4096).decode()
            aux = pedido.buscar_todos_horarios(str(dia))
            if aux:
                enviar = ','.join(aux)
                con.send('1'.encode())
                con.send(enviar.encode())
            else:
                con.send('0'.encode())
        
        elif mensagem == '12':
            cpf = con.recv(4096).decode()
            datas = pedido.buscar_todas_datas_cliente(int(cpf))
            if datas:
                elementos = [dado.replace('(', '').replace(')', '').replace(',', '') for dado in datas]
                datas_str = ''.join(elementos)
                con.send('1'.encode())
                con.send(datas_str.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '13':
            dados = con.recv(4096).decode()
            partes = dados.split(',')
            if pedido.delete_reserva(int(partes[0]), partes[1]):
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        

        if mensagem == '14':
            dados = pedido.buscar_todos_dados()
            if dados:
                enviar = ''.join(dados)
                con.send('1'.encode())
                con.send(enviar.encode())
            else:
                con.send('0'.encode())
        

        elif mensagem == '15':
            if h.drop_tabela_data():
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        
        elif mensagem == '16':
            aux = pedido.contar_pedidos_cadastrados()
            con.send(str(aux).encode())
        
        elif mensagem == '17':
            cpf = con.recv(4096).decode()
            aux = cli.buscar_email_cpf(int(cpf))
            if aux != None:
                con.send('1'.encode())
                con.send(str(aux).encode())
            else:
                con.send('0'.encode())

        


    print(f'Encerrando conexão.')
    con.close()
    print(f'Servidor on.')

def main():
    print('Servidor on.')
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.bind(addr)
    serv_socket.listen()

    while True:
        con, cliente = serv_socket.accept()
        thread = threading.Thread(target=menu, args=(con, cliente))
        thread.start()

if __name__ == "__main__":
    main()
