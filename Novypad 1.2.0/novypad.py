import PySimpleGUI as sg
sg.ChangeLookAndFeel('DarkBrown')

WIN_W: int = 90
WIN_H: int = 25
filename:str = None

file_new: str = 'New NovyTxt.............(CTRL+N)'
file_open: str = 'Open..............(CTRL+O)'
file_save: str = 'Save............(CTRL+S)'

menu_layout: list = [['File', [file_new, file_open, file_save, 'Save as', '---', 'Leave']],
                     ['Settings', ['Word counter']],
                     ['Help', ['About']]]

layout: list = [[sg.Menu(menu_layout)],
                [sg.Text('> New NovyTxt <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
                [sg.Multiline(font=('Consolas', 12), size=(WIN_W, WIN_H), key='_BODY_')]]

window: object = sg.Window('NovyPad 1.2.0', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True)
window.read(timeout=1)
window['_BODY_'].expand(expand_x=True, expand_y=True)

def new_file() -> str:
    ''' Reset body and info bar, and clear filename variable '''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New NovyTxt <')
    filename = None
    return filename

def open_file() -> str:
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

def save_file(filename: str):
    ''' Save file instantly if already open; otherwise use `save-as` popup '''
    if filename not in (None, ''):
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
        window['_INFO_'].update(value=filename)
    else:
        save_file_as()

def save_file_as() -> str:
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

def word_count():
    ''' Display estimated word count '''
    words: list = [w for w in values['_BODY_'].split(' ') if w!='\n']
    word_count: int = len(words)
    sg.PopupQuick('Total words: {:,d}'.format(word_count), auto_close=False)

def about_me():
    sg.PopupQuick('Author: LdmasterKen, Version 1.2.0', auto_close=False)

while True:
    event, values = window.read()

    if event in (None, 'Leave'):
        break
    if event in (file_new, 'n:78'):
        filename = new_file()
    if event in (file_open, 'o:79'):
        filename = open_file()
    if event in (file_save, 's:83'):
        save_file(filename)
    if event in ('Save as',):
        filename = save_file_as()
    if event in ('Word counter',):
        word_count()
    if event in ('About',):
        about_me()