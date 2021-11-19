import sys
from time import sleep
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def chat( event, values, state, user_manager):
    '''
    This function send a message to JSNDrop storage to be displayed in linked des screens.
    '''
    cont = True
    if event == "Send":   
        message = values['message']
        result = user_manager.chat(message)
        sg.Popup(result, keep_on_top=True)
    else:
        cont = True
    return cont 