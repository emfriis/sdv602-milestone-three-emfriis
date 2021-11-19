import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import controller.login.login_button as login_button
import controller.login.register_button as register_button
import controller.login.exit_button as exit_button

class login_layout(object):
    
    def __init__(self):
        self.window = None
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        
    def self_layout(self, **kwargs):
        sg.theme('Dark Blue 3')
        
        self.components['username'] = sg.Input('', key='username')
        self.components['password'] = sg.Input('', key='password', password_char='*')
        
        self.components['login_button'] = sg.Button(button_text = 'Log In')
        self.controls += [login_button.login]
        
        self.components['register_button'] = sg.Button(button_text = 'Register')
        self.controls += [register_button.register]
        
        self.controls += [exit_button.exit]
        
        self.layout = [
            [sg.Text('Username')],
            [self.components['username']],
            [sg.Text('Password')],
            [self.components['password']],
            [self.components['login_button'],self.components['register_button']]
        ]
        
    def render(self):
        if self.layout != []:
            self.window = sg.Window('Login', self.layout, grab_anywhere=False, finalize=True)
            
    def listen(self):
        if self.window != None:
            cont = True
            while cont == True:
                event, values = self.window.read()
                for control in self.controls:
                    cont = control(event, values, {'view':self})
            self.window.close()