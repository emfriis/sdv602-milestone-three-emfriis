import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import controller.register.register_button as register_button
import controller.login.exit_button as exit_button

class register_layout(object):
    
    def __init__(self):
        self.window = None
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        
    def self_layout(self, **kwargs):
        sg.theme('Dark Blue 3')
        
        self.components['email'] = sg.Input('', key='email')
        self.components['username'] = sg.Input('', key='username')
        self.components['password'] = sg.Input('', key='password', password_char='*')
        
        self.components['register_button'] = sg.Button(button_text = 'Register')
        self.controls += [register_button.register]
        
        self.controls += [exit_button.exit]
        
        self.layout = [
            [sg.Text('Email')],
            [self.components['email']],
            [sg.Text('Username')],
            [self.components['username']],
            [sg.Text('Password')],
            [self.components['password']],
            [self.components['register_button']]
        ]
        
    def render(self):
        if self.layout != []:
            self.window = sg.Window('Register', self.layout, grab_anywhere=False, finalize=True)
            
    def listen(self):
        if self.window != None:
            cont = True
            while cont == True:
                event, values = self.window.read()
                for control in self.controls:
                    cont = control(event, values, {'view':self})
            self.window.close()