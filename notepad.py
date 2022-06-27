
from os import link
import PySimpleGUI as sg
import pathlib
sg.theme("Dark")

WIN_W = 90
WIN_H = 25
file = None

#Layout 

menu_layout = [['Inicio', ['Novo (Ctrl+N)', 'Abrir (Ctrl+O)', 'Salvar (Ctrl+S)', 'Salvar como', '---', 'Sair']],
            ['Ferramentas', ['contar palavras']],
            ['Ajuda', ['Sobre']]]

layout = [[sg.Menu(menu_layout)],
        [sg.Text('> Escreva Seu texto <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
        [sg.Multiline(font=('Consolas', 16), size=(WIN_W, WIN_H), key='_BODY_')]]

# janela
window = sg.Window('Agenda de Anotações', layout=layout, margins=(0.5,0.5), resizable=True, return_keyboard_events=True, finalize=True)
window.maximize()
window['_BODY_'].expand(expand_x=True, expand_y=True)


#definições e ações
def new_file():
    '''Reset body and info bar, and clear filename variable'''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New File <')
    file = None
    return file

def open_file():
    '''Open file and update the infobar'''
    filename = sg.popup_get_file('Open', no_window=True)
    if filename:
        file = pathlib.Path(filename)
        window['_BODY_'].update(value=file.read_text())
        window['_INFO_'].update(value=file.absolute())
        return file

def save_file(file):
    '''Save file instantly if already open; otherwise use `save-as` popup'''
    if file:
        file.write_text(values.get('_BODY_'))
    else:
        save_file_as()

def save_file_as():
    '''Save new file or save existing file with another name'''
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
    if filename:
        file = pathlib.Path(filename)
        file.write_text(values.get('_BODY_'))
        window['_INFO_'].update(value=file.absolute())
        return file

def word_count():
    '''Display estimated word count'''
    words = [w for w in values['_BODY_'].split(' ') if w!='\n']
    word_count = len(words)
    sg.popup_no_wait('Quantidade: {:,d}'.format(word_count))

def about_me():
    '''A short, pithy quote'''
    sg.popup_no_wait('estes é um programa de aprendizagem')

#evento de loop 
while True:
    event, values = window.read()
    if event in('Sair', None):
        break
    if event in ('Novo (Ctrl+N)', 'n:78'):
        file = new_file()
    if event in ('Abrir (Ctrl+O)', 'o:79'):
        file = open_file()
    if event in ('Salvar (Ctrl+S)', 's:83'):
        save_file(file)
    if event in ('Salvar como',):
        file = save_file_as()   
    if event in ('contar palavras',):
        word_count() 
    if event in ('Sobre',):
        about_me()

