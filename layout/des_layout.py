import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import glob
import controller.des.exit_button as exit_button
import controller.des.new_button as new_button

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
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        self.figure_agg = None
        self.data_frame = pd.DataFrame()
        self.data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\data_source"
    
    def self_layout(self, **kwargs):
        '''
        The function to instantiate the elements & layout for des_layout.
        '''
        sg.theme('Dark Blue 3')
        figure_w, figure_h = 650, 650
        
        self.components['figure_select'] =  sg.Button(button_text = 'Select CSV File')
        
        self.components['figure_upload'] = sg.Button(button_text = 'Upload CSV File')
        
        self.components['new_button'] = sg.Button(button_text = 'New DES')
        self.controls += [new_button.new]
        
        self.controls += [exit_button.exit]
        
        self.layout = [
            [self.components['figure_select'],self.components['figure_upload']],
            [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
            [sg.Text('Chat Placeholder')],
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
    
    def render(self):
        '''
        The function to render the current instance of des_layout.
        '''
        if self.layout != []:
            self.window = sg.Window('Data Explorer', self.layout, grab_anywhere=False, finalize=True)
    
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
                if event == 'Upload CSV File':
                    file_path = sg.PopupGetFile('Please select a data source', file_types=(("CSV Files", "*.csv"),), initial_folder="C:\\")
                    if file_path:
                        if not glob.glob(self.data_path + "\{}".format(os.path.basename(file_path))):
                            shutil.copy(file_path, self.data_path)
            self.window.close()
            