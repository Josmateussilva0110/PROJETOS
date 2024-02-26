import re
from email.message import EmailMessage
from datetime import datetime
import smtplib

def extrair_informacoes_datas(data_str):
    if not data_str:
        return None
    else:
        info = {}
        linhas = data_str.split('\n')
        for linha in linhas:
            if ':' in linha:
                chave, valor = linha.split(': ', 1)
                if chave in info:
                    info[chave].append(valor)
                else:
                    info[chave] = [valor]
        return info

def formatar_informacoes_data(info):
    if not info:
        return None
    else:
        formatado = list()
        for chave, valores in info.items():
            for valor in valores:
                valor_sem_aspas = re.sub(r"'", '', valor)
                formatado.append(f"{chave}: {valor_sem_aspas}")
        return formatado


def email_valido(email):
    # Padrão de expressão regular para validar um endereço de e-mail
    email_valido = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # Verifica se o email corresponde ao padrão
    if re.match(email_valido, email):
        return 1
    else:
        return 0

def verificar_valor_inteiro(arg):
    try:
        if arg.isnumeric() and int(arg) >=0:
            return True
    except ValueError:
        return False


def verificar_nome(arg):
    if arg.replace(' ', '').isalpha():
        return 1
    else:
        return 0
    
def verificar_espacos(valor1, valor2, valor3):
    if valor1 == '' or valor2 == '' or valor3 == '':
        return True
    else:
        return False


def validacao(cpf, nome, email):
    if not verificar_valor_inteiro(cpf) or not verificar_nome(nome) or not email_valido(email):
        return False
    if verificar_espacos(cpf, nome, email):
        return False
    return True


def EnviaEmail(destinatario,mensagem):
    # Configurar email e senha
    EMAIL_ADDRESS = 'cineplus.gerencia@gmail.com'
    EMAIL_PASSWORD = 'qyskmjhoyapdvjay'

    # Criar um email...
    msg = EmailMessage()
    msg['Subject'] = 'COMPROVANTE DE AGENDA'
    msg['From'] = 'cineplus.gerencia@gmail.com'
    msg['To'] = destinatario
    msg.set_content(mensagem)

    # Ecnviar email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg) 


def formatar_mensagem(dados_cliente, dia, horario):
    formato_mensagem = "cliente: {}\nDia: {}\nHorario: {}\nEmitido: {}"
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    emissao = data_e_hora_em_texto
    mensagem_formatada = formato_mensagem.format(dados_cliente, dia, horario, emissao)
    return mensagem_formatada
