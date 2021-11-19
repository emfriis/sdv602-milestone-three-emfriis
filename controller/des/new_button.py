import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def new(event, values, state, user_manager):
    '''
    This button opens a new window with another des gui.
    '''
    from layout.des_layout import des_layout
    keep_going = True
    if event == 'New DES':
        des_layout_view = des_layout(user_manager)
        des_layout_view.self_layout()
        des_layout_view.render()
        des_layout_view.listen()
    return keep_going 