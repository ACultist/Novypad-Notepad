import PySimpleGUI as sg
import os
from os import remove
from PySimpleGUI.PySimpleGUI import Window, theme


#Biblioteca adicional
def getUsername():
    """
    -> Função para pegar o nome de usuário do computador.
    """
    return os.getlogin()


def exist(name):
    """
    -> Função para verificar a existência de um arquivo no mesmo local localizado o programa.
    :param name: Nome do arquivo para fazer a verificão.
    """
    try:
        a = open(name, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def create(name, error='ERRO: Não foi possível criar o arquivo.'):
    """
    -> Função para criar um arquivo no mesmo local localizado o programa.
    :param name: Nome do arquivo para fazer a criação.
    :param error: (Opcional) O que mostrar caso a função dê erro.
    """
    try:
        a = open(name, 'wt+')
        a.close()
    except:
        print(f'\033[31m{error}\033[m')


def read(name, error='ERRO: Não foi possível ler o arquivo.'):
    """
    -> Função para ler um arquivo no mesmo local localizado o programa.
    :param name: Nome do arquivo para fazer a leitura.
    :param error: (Opcional) O que mostrar caso a função dê erro.
    """
    try:
        a = open(name, 'rt')
    except:
        print(f'\033[31m{error}\033[m')
    else:
        return a.read()
    finally:
        a.close()


def write(name, write='', error='ERRO: Não foi possível editar o arquivo.'):
    """
    -> Função para escrever algo em um arquivo no mesmo local localizado o programa.
    :param name: Nome do arquivo a qual será usado para fazer a escrita.
    :param write: Valor que será digitado no arquivo.
    :param error: (Opcional) O que mostral caso a função dê erro.
    """
    try:
        a = open(name, 'at')
    except:
        print(f'\033[31m{error}\033[m')
    else:
        a.write(write)


def delete(name):
    """
    -> Função para deletar um arquivo no mesmo local localizado o programa.
    :param name: Nome do arquivo a qual será deletado.
    """
    remove(name)


#Biblioteca original
def new_file(window) -> str:
    ''' Reset body and info bar, and clear filename variable '''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New NovyTxt <')
    filename = None
    return filename


def open_file(window) -> str:
    ''' Open file and update the infobar '''
    try:
        filename: str = sg.popup_get_file('Open NovyTxt', no_window=True)
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        with open(filename, 'r') as f:
            window['_BODY_'].update(value=f.read())
        window['_INFO_'].update(value=filename)
    return filename


def save_file(window, values, filename):
    ''' Save file instantly if already open; otherwise use `save-as` popup '''
    if filename not in (None, ''):
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
        window['_INFO_'].update(value=filename)
    else:
        save_file_as(window, values)


def save_file_as(window, values):
    ''' Save new file or save existing file with another name '''
    try:
        filename: str = sg.popup_get_file('Save Novy', save_as=True, no_window=True)
    except:
        return
    if filename not in (None, '') and not isinstance(filename, tuple):
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
            window['_INFO_'].update(value=filename)
    return filename


def word_count(values):
    ''' Display estimated word count '''
    words: list = [w for w in values['_BODY_'].split(' ') if w!='\n']
    word_count: int = len(words)
    sg.PopupQuick('Total words: {:,d}'.format(word_count), auto_close=False)


def createWindow(msg, window='Window'):
    """
    -> Função para criar uma janela simples.
    :param msg: Mensagem para mostrar na janela.
    :param window: (Opcional) Nome da janela.
    """
    sg.PopupQuick(msg, title=window, auto_close=False)


#Biblioteca adicional
def changeTheme(file, theme):
    """
    -> Função para trocar o tema do programa.
    :param file: Nome do arquivo que está salvo o tema atual.
    :param theme: Novo tema a ser usado.
    """
    #Corrigindo erro do atual
    if ' (atual)' in theme:
        return

    if exist(file):
        delete(file)

    create(file)
    write(file, theme)

    createWindow('To change your theme please restart the program.')


def themeEvent(event, themes):
    """
    -> Função para verificar se algum tema foi escolhi na tela de opções de temas e altera-lo.
    :param event: Evento da biblioteca sg (PySimpleGUI).
    :param themes: Opções de temas.
    """
    for item in themes:
        if event in item:
            changeTheme('theme.txt', item)
            return True
    
    return False


def createThemesWindowButton(list, name='Window'):
    """
    -> Função para criar uma janela com opções de temas.
    :param list: Opções de temas a serem escolhidos.
    :param name: (Opcional) Nome da janela
    """
    layout = [[]]
    cont = 0
    linha = 0
    for tema in list:
        layout[linha].append(sg.Button(list[cont]))
        cont += 1
        if cont % 3 == 0:
            layout.append([])
            linha += 1
    
    while True:
        event, values = sg.Window('Themes', layout, auto_close=False).read(close=True)
        if themeEvent(event, list):
            return