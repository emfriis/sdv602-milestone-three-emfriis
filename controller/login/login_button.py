import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def login(event, values, state):
    '''
    This function logs a user in after validating their credentials with jsnDrop remote storage.
    If the credentials are valid, a new window with the des gui is opened.
    '''
    from layout.des_layout import des_layout
    cont = True
    if event == 'Log In':
        from data.user_manager import UserManager
        user_manager = UserManager()
        username = values['username']
        password = values['password']
        result = user_manager.login(username, password)
        sg.Popup(result, keep_on_top=True)
        if result == "Login Success":
            des_layout_view = des_layout(user_manager)
            des_layout_view.self_layout()
            des_layout_view.render()
            des_layout_view.listen()
    return cont