import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def register(event, values, state):
    '''
    This function registers a new user in jsnDrop remote storage if the new user credentials are valid.
    '''
    cont = True
    if event == 'Register':
        from data.user_manager import UserManager
        user_manager = UserManager()
        email = values['email']
        username = values['username']
        password = values['password']
        result = user_manager.register(username,email,password)
        sg.Popup(result, keep_on_top=True)
    return cont