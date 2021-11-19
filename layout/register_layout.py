import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import controller.register.register_button as register_button
import controller.login.exit_button as exit_button

class register_layout(object):
    '''
    A class representing a registration screen.
    
    Attributes:
        window: the window the register gui layout is applied to.
        layout: the list of elements comprising the register gui.
        components: the elements that comprise the register gui.
        controls: the event-triggered controllers linked to the register gui.
    '''
    
    def __init__(self):
        '''
        The constructor for register_layout.
        '''
        self.window = None
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        
    def self_layout(self, **kwargs):
        '''
        The function to instantiate the elements & layout for register_layout.
        '''
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
        '''
        The function to render the current instance of register_layout.
        '''
        if self.layout != []:
            self.window = sg.Window('Register', self.layout, grab_anywhere=False, finalize=True)
            
    def listen(self):
        '''
        The function to start the event loop for the current instance of register_layout.
        '''
        if self.window != None:
            cont = True
            while cont == True:
                event, values = self.window.read()
                for control in self.controls:
                    cont = control(event, values, {'view':self})
            self.window.close()