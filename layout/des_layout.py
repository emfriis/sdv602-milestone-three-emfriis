import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import glob
import controller.des.exit_button as exit_button
import controller.des.new_button as new_button
import controller.des.chat_button as chat_button
import threading
from threading import Thread
import time
import signal

class des_layout(object):
    '''
    A class representing a data explorer screen.
    
    Attributes:
        window: the window the des gui layout is applied to.
        user_manager: an object representing the current user's statuses.
        layout: the list of elements comprising the des gui.
        components: the elements that comprise the des gui.
        controls: the event-triggered controllers linked to the des gui.
        figure_agg: the current matplotlib figure.
        data_frame: the current pandas dataframe.
        data_path: the path of the data source folder.
    '''
    
    def __init__(self, user_manager):
        '''
        The constructor for des_layout.
        '''
        self.window = None
        self.user_manager = user_manager
        self.jsnDrop = user_manager.jsnDrop
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        self.figure_agg = None
        self.data_frame = pd.DataFrame()
        self.data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\data_source"
        self.chat_count = 0
        self.exit_event = threading.Event() 
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def self_layout(self, **kwargs):
        '''
        The function to instantiate the elements & layout for des_layout.
        '''
        sg.theme('Dark Blue 3')
        
        self.components['chatbox'] = sg.Multiline('Chatbox', autoscroll=False, disabled=True, key='chatbox', size=(50,10))
        
        self.components['message'] = sg.Input('', key='message')
        
        self.components['figure_select'] =  sg.Button(button_text = 'Select CSV File')
        
        self.components['figure_upload'] = sg.Button(button_text = 'Upload CSV File')
        
        self.components['new_button'] = sg.Button(button_text = 'New DES')
        self.controls += [new_button.new]
        
        self.components['chat_button'] = sg.Button(button_text = 'Send')
        self.controls += [chat_button.chat]
        
        self.controls += [exit_button.exit]
        
        self.layout = [
            [self.components['figure_select'],self.components['figure_upload']],
            [sg.Canvas(key='-CANVAS-', size=(450,450))],
            [self.components['chatbox']],
            [self.components['message'],self.components['chat_button']],
            [self.components['new_button']]
        ]
    
    def draw_figure(self, canvas, figure):
        '''
        The function to draw the current selected figure for des_layout.
        '''
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def delete_figure_agg(self):
        '''
        The function to delete the current figure for des_layout.
        '''
        if self.figure_agg:
            self.figure_agg.get_tk_widget().forget()
        plt.close('all')
        
    def signal_handler(self, signum, frame):
        '''
        The function to set the handler for asynchronous events.
        '''
        self.exit_event.set()   

    def set_up_chat_thread(self):
        '''
        The function to instatiate the chat thread.
        '''
        self.user_manager.chat_thread = Thread(target=self.chat_display_update,args=([self.user_manager]))
        self.user_manager.chat_thread.setDaemon(True)
        self.user_manager.stop_thread = False
        self.user_manager.chat_thread.start()

    def chat_display_update(self, user_manager):
        '''
        The function to update the chat display for the current des.
        '''
        time.sleep(2)

        if self.window != None:
            self.chat_count += 1
            result = self.jsnDrop.select("tblChat",f"DESID = '{user_manager.current_screen}'")
            
            if result != "Data error. Nothing selected from tblChat":
                messages = ""
                sorted_chats = sorted(result,key = lambda i : i['Time'] )
                for record in sorted_chats:
                    new_display = ""
                    if not (user_manager.latest_time is None):
                        if record['Time'] > user_manager.latest_time:
                            new_display = f"{record['PersonID']} : [{record['Chat']}]\n"
                    else:
                        new_display = f"{record['PersonID']} : [{record['Chat']}]\n"
                    messages += new_display

                user_manager.chat_list = [messages]
                if len(user_manager.chat_list) > 5:
                    user_manager.chat_list = user_manager.chat_list[:-5]
                
                # Makes a string of messages to update the display
                Update_Messages = ""
                for messages in user_manager.chat_list:
                    Update_Messages += messages
                
                # Send the Event back to the window if we haven't already stopped
                if not user_manager.stop_thread:

                    # Time stamp the latest record
                    if len(sorted_chats) > 1:
                        latest_record = sorted_chats[:-1][0]
                    else:
                        latest_record = sorted_chats[0]
                    user_manager.latest_time = latest_record['Time']

                    # Send the event back to the window
                    self.window.write_event_value('-CHATTHREAD-', Update_Messages)
        # The Thread stops - no loop - when the event is caught by the Window it starts a new long task
    
    def render(self):
        '''
        The function to render the current instance of des_layout.
        '''
        if self.layout != []:
            self.window = sg.Window('Data Explorer', self.layout, size=(750,750), grab_anywhere=False, finalize=True)
    
    def listen(self):
        '''
        The function to start the event loop for the current instance of des_layout.
        '''
        if self.window != None:
            cont = True
            while cont == True:
                event, values = self.window.read()
                for control in self.controls:
                    cont = control(event, values, {'view':self}, self.user_manager)
                if event == 'Select CSV File':
                    file_path = sg.PopupGetFile('Please select a data source', file_types=(("CSV Files", "*.csv"),), initial_folder=self.data_path)
                    if file_path:
                        self.delete_figure_agg()
                        self.data_frame = pd.read_csv(file_path).pivot('place', 'group', 'count')
                        data_plot = self.data_frame.plot(kind='line')
                        fig = plt.gcf()
                        self.figure_agg = self.draw_figure(self.window['-CANVAS-'].TKCanvas, fig)
                        self.user_manager.set_current_DES(os.path.basename(file_path))
                        self.set_up_chat_thread()
                if event == 'Upload CSV File':
                    file_path = sg.PopupGetFile('Please select a data source', file_types=(("CSV Files", "*.csv"),), initial_folder="C:\\")
                    if file_path:
                        if not glob.glob(self.data_path + "\{}".format(os.path.basename(file_path))):
                            shutil.copy(file_path, self.data_path)
                if event == "Exit" :
                    self.user_manager.stop_thread = True
                elif event == "-CHATTHREAD-" and not self.user_manager.stop_thread:
                    self.user_manager.stop_thread = True
                    self.window['chatbox'].Update(values[event])
                    if self.user_manager.stop_thread:
                        self.user_manager.stop_thread = False
                        self.set_up_chat_thread()
            self.window.close()