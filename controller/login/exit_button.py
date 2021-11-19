import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def exit(event, values, state):
    '''
    This function exits the current window.
    '''
    cont = True
    if event in (sg.WIN_CLOSED, 'Exit'):
        cont = False
    else:
        cont = True
    
    return cont