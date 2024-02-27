from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from pygame.locals import USEREVENT  

import pygame
from pygame import mixer
import os


cor_0 = "#f0f3f5"
cor_1 = "#feffff"
cor_2 = "#3fb5a3"
cor_3 = "#2e2d2c"
cor_4 = "#403d3d"
cor_5 = "#4a88e8"


janela = Tk()
janela.title("Music_player")
janela.geometry('352x255')
janela.configure(background=cor_1)
janela.resizable(width=False, height=False)
pygame.init()
mixer.init()

frame_left = Frame(janela, width=120, height=120, bg=cor_3)
frame_left.grid(row=0, column=0, pady=1, padx=1, sticky=NSEW)


frame_right = Frame(janela, width=250, height=150, bg=cor_3)
frame_right.grid(row=0, column=1, pady=1, padx=0, sticky=NSEW)


frame_down = Frame(janela, width=404, height=100, bg=cor_3)
frame_down.grid(row=1, columnspan=3, pady=1, padx=0, sticky=NSEW)


#frame right
list_box = Listbox(frame_right,width= 26,height=10, selectmode=SINGLE, font=('arial 9 bold'), bg=cor_3, fg=cor_1)
list_box.grid(row=0, column=0)
scroll = Scrollbar(frame_right)
scroll.grid(row=0, column=4, sticky=NSEW)
list_box.config(yscrollcommand=scroll.set)
scroll.config(command=list_box.yview)




#frame down
current_music = Label(frame_down, text='Selecione uma musica', width=44, justify=LEFT, anchor='nw', font=('arial 10'), bg=cor_1, fg=cor_4)
current_music.place(x=0, y=1)


# frame left
img_01 = Image.open('imagens/Music_icon.png')
img_01 = img_01.resize((110, 110))
img_01 = ImageTk.PhotoImage(img_01)

logo = Label(frame_left, height=130, image=img_01, compound=LEFT, padx=10, anchor='nw', font=('arial 16 bold'), bg=cor_3, fg=cor_3)
logo.place(x=18, y=15)




#functions
diretorio = os.getcwd()
def prox_music():
    tocando = current_music['text']
    index = lista.index(tocando)
    new_index = (index + 1) % len(lista) 
    tocando = lista[new_index]
    current_music['text'] = tocando
    list_box.delete(0, END)
    mostrar()
    list_box.select_set(new_index)
    list_box.config(selectmode=SINGLE)
    mixer.music.load(tocando)
    mixer.music.play()

def play_music():
    rodando = list_box.get(ACTIVE)
    current_music['text'] = rodando
    mixer.music.load(rodando)
    mixer.music.play()



def ant_music():
    tocando = current_music['text']
    index = lista.index(tocando)
    new_index = index-1
    if new_index < 0:
        new_index = len(lista) -1
    tocando = lista[new_index]
    mixer.music.load(tocando)
    mixer.music.play()
    list_box.delete(0, END)
    mostrar()
    list_box.select_set(new_index)
    list_box.config(selectmode=SINGLE)
    current_music['text'] = tocando


def pausar():
    pygame.mixer.music.pause()


def retornar():
    pygame.mixer.music.unpause()


def explorar_arquivos():
    global diretorio, lista  
    diretorio_selecionado = filedialog.askdirectory()
    if diretorio_selecionado:
        diretorio_selecionado = diretorio_selecionado.replace('/', '\\')
        os.chdir(diretorio_selecionado)
        diretorio = diretorio_selecionado 
        list_box.delete(0, END)
        lista = os.listdir(diretorio)  
        mostrar()
    



img_02 = Image.open('imagens/left_icon.png')
img_02 = img_02.resize((30, 30))
img_02 = ImageTk.PhotoImage(img_02)
button_left = Button(frame_down,command=ant_music, width=40, height=40,image=img_02, font=('arial 10 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1)
button_left.place(x=45, y=35)

img_04 = Image.open('imagens/pause_icon.png')
img_04 = img_04.resize((30, 30))
img_04 = ImageTk.PhotoImage(img_04)
button_pause = Button(frame_down, command=pausar, width=40, height=40,image=img_04, font=('arial 10 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1)
button_pause.place(x=90, y=35)

img_05 = Image.open('imagens/play_icon.png')
img_05 = img_05.resize((30, 30))
img_05 = ImageTk.PhotoImage(img_05)
button_play = Button(frame_down, command=play_music, width=40, height=40,image=img_05, font=('arial 10 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1)
button_play.place(x=135, y=35)

img_06 = Image.open('imagens/des_pause_icon.png')
img_06 = img_06.resize((30, 30))
img_06 = ImageTk.PhotoImage(img_06)
button_play = Button(frame_down, command=retornar, width=40, height=40,image=img_06, font=('arial 10 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1)
button_play.place(x=180, y=35)


img_03 = Image.open('imagens/right_icon.png')
img_03 = img_03.resize((30, 30))
img_03 = ImageTk.PhotoImage(img_03)
button_right = Button(frame_down, command=prox_music, width=40, height=40,image=img_03, font=('arial 10 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1)
button_right.place(x=225, y=35)


button_explore = Button(frame_down, text="Explore", width=9, height=3, font=('arial 7 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1, command=explorar_arquivos)
button_explore.place(x=287, y=35) 


def mostrar():
    list_box.delete(0, END) 
    for i in lista:
        if i.lower().endswith('.mp3'):
            list_box.insert(END, i)

if diretorio:
    lista = os.listdir(diretorio)
    mostrar()

mixer.music.set_endevent(USEREVENT + 1) 

def check_music_end():
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == mixer.music.get_endevent():
            prox_music()
    janela.after(100, check_music_end)

janela.after(100, check_music_end)


janela.mainloop()
