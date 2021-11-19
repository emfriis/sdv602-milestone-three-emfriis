import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import controller.login.login_button as login_button
import controller.login.register_button as register_button
import controller.login.exit_button as exit_button

class login_layout(object):
    '''
    A class representing a login screen.
    
    Attributes:
        window: the window the login gui layout is applied to.
        layout: the list of elements comprising the login gui.
        components: the elements that comprise the login gui.
        controls: the event-triggered controllers linked to the login gui.
    '''
    
    def __init__(self):
        '''
        The constructor for login_layout.
        '''
        self.window = None
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        
    def self_layout(self, **kwargs):
        '''
        The function to instantiate the elements & layout for login_layout.
        '''
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
        '''
        The function to render the current instance of login_layout.
        '''
        if self.layout != []:
            self.window = sg.Window('Login', self.layout, grab_anywhere=False, finalize=True)
            
    def listen(self):
        '''
        The function to start the event loop for the current instance of login_layout.
        '''
        if self.window != None:
            cont = True
            while cont == True:
                event, values = self.window.read()
                for control in self.controls:
                    cont = control(event, values, {'view':self})
            self.window.close()