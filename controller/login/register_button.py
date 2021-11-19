import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def register(event, values, state):
    '''
    This function opens a new window with the register gui.
    '''
    from layout.register_layout import register_layout
    cont = True
    if event == 'Register':
        register_layout_view = register_layout()
        register_layout_view.self_layout()
        register_layout_view.render()
        register_layout_view.listen()
    return cont