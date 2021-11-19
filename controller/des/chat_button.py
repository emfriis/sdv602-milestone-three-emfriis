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
        from data.user_manager import UserManager
        user_manager = UserManager()
        message = values['message']
        user_manager.chat(message)
    else:
        keep_going = True
    return keep_going 