import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import controller.des.exit_button as exit_button
import controller.des.new_button as new_button
import controller.des.upload_button as upload_button
from data.user_manager import UserManager

class des_layout(object):
    
    def __init__(self, user_manager):
        self.window = None
        self.user_manager = user_manager
        self.layout = []
        self.components = {'components': False}
        self.controls = []
        self.figure_agg = None
        self.data_frame = pd.DataFrame()
    
    def self_layout(self, **kwargs):
        sg.theme('Dark Blue 3')
        figure_w, figure_h = 650, 650
        
        self.components['figure_select'] =  sg.Button(button_text = 'Select CSV File')
        
        self.components['figure_upload'] = sg.Button(button_text = 'Upload CSV File')
        
        self.components['new_button'] = sg.Button(button_text = 'New DES')
        self.controls += [new_button.new]
        
        self.components['upload_button'] = sg.Button(button_text = 'Upload CSV')
        self.controls += [upload_button.upload]
        
        self.controls += [exit_button.exit]
        
        self.layout = [
            [self.components['figure_select'],self.components['figure_upload']],
            [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
            [sg.Text('Chat Placeholder')],
            [self.components['new_button'],self.components['upload_button']]
        ]
    
    def fig_draw(self, values): 
        if self.current_csv(values) :
            choice = values['-LISTBOX-'][0]
    
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def delete_figure_agg(self):
        if self.figure_agg:
            self.figure_agg.get_tk_widget().forget()
        plt.close('all')
    
    def render(self):
        if self.layout != []:
            self.window = sg.Window('Data Explorer', self.layout, grab_anywhere=False, finalize=True)
    
    def listen(self):
        if self.window != None:
            cont = True
            while cont == True:
                event, values = self.window.read()
                for control in self.controls:
                    cont = control(event, values, {'view':self}, self.user_manager)
                if event == 'Select CSV File':
                    file_path = sg.PopupGetFile('Please select a data source', file_types=(("CSV Files", "*.csv"),), initial_folder=r"../data_source/")
                    if file_path:
                        self.delete_figure_agg()
                        self.data_frame = pd.read_csv(file_path).pivot('place', 'group', 'count')
                        data_plot = self.data_frame.plot(kind='line')
                        fig = plt.gcf()
                        self.figure_agg = self.draw_figure(self.window['-CANVAS-'].TKCanvas, fig)
                if event == 'Upload CSV File':
                    file_path = sg.PopupGetFile('Please select a data source', file_types=(("CSV Files", "*.csv"),), initial_folder=r"C:\\")
            self.window.close()
            