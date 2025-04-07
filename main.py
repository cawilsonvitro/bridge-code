#region Imports
import tkinter as tk
from tkinter import Misc
import tkinter.ttk as ttk
from old_thorlabs import *
from gui import *
import json
import os
import time 
import numpy as np
import csv
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from multiprocessing import Process, Queue
import threading


#endregion 

class resistain_app:

    #region Application control
    def __init__(self):
        '''
        intit. class for use
        '''
        self.quit = False
        self.process_display = None
        self.conc = None

        #spectometer
        self.spectrometer = None
        self.integration_time = None
        self.model = None

        #dark sample
        self.dark_intens = None
        self.dark = False

        #light sample
        self.light_intens = None

        #config storage
        self.config = None
        self.spec_config = None

        #avgs 
        self.light_avg = None
        self.dark_avg = None
        self.dark_intens_avg = None
        self.light_intens = None
        self.boxcar = None
        self.adjust = None

        #data management
        self.startPt = None
        self.stopPt = None
        self.dataPath = r"data/"
        self.sample_num = 1
        self.exst = ".csv"
        
        #threading management not usable yet
        #self.spectrometerThread = threading.Thread(target=)

    def startApp(self):
        '''
        starts tk application
        '''
        self.root = tk.Tk()
        self.root.title("Resistain App")
        self.root.geometry("480x400")
        self.root.resizable(width=False,height=False)
        self.root.bind("<Escape>", self.endApp)
        self.root.protocol("WM_DELETE_WINDOW",self.endProto)
        self.process_display = tk.StringVar() 
        self.process_display.set("Booting")
        self.conc = tk.StringVar()
        self.conc_pre = "Concentration : "

    #building graph window
        self.graphwindow = tk.Toplevel(self.root)
        self.graphwindow.geometry("600x600")
        self.graphwindow.resizable(width=False, height=False)
        self.graphwindow.configure(bg="#FFFFFF")
        self.graphwindow.protocol("WM_DELETE_WINDOW", self.endProto)
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.graphwindow)
        self.canvas.get_tk_widget().grid(column=0, row=1)
        plt.gcf().subplots(1, 1)

        self.graphwindow.update()



        self.conc.set( self.conc_pre + "0")
        self.buildGUI(self.root)
        self.root.mainloop()
    
    def endProto(self):
        '''
        wrapper to endApp
        '''
        self.endApp(None)
    
    def endApp(self, event):
        '''
        ends application
        '''
        self.quit = True
        self.root.quit()
        # self.spectrometer.quit()
        
    #endregion

    #region GUI building
    

    def buildGUI(self,root):
        '''
        builds gui for user interaction
        '''
        Button.remove(None)
        StandardInput.remove(None)
        Label.remove(None)
        StandardLabel.remove(None)

        StandardButtons(
            "Dark_Sample",
            root,
            image = TkImage("Dark_Sample", r"images/Dark_Sample.jpg").image,
            command = self.take_dark
        ).place(x = 30,y = 25)

        StandardButtons(
            "Light_Sample",
            root,
            image = TkImage("Light_Sample", r"images/Light_Sample.png").image,
            command = self.take_data
        ).place(x = 30,y = 85)
        
        StandardButtons(
            "Save",
            root,
            image = TkImage("Save", r"images/Save.png").image,
            command = self.save
        ).place(x = 30, y = 145)




        Label(
            "Process_Status", 
            root,
            textvariable = self.process_display,
            anchor=tk.W,           
            height=1,              
            width=30,              
            bd=1,                  
            font=("Arial", 10), 
            cursor="hand2",   
            fg="black",                           
            justify = tk.LEFT,  
            wraplength=100   
            ).place(x = 300, y = 85, width = 180,height = 200)
        
        Label(
            "Conc_value", 
            root,
            textvariable = self.conc,
            anchor=tk.W,           
            height=1,              
            width=30,              
            bd=1,                  
            font=("Arial", 10), 
            cursor="hand2",   
            fg="black",                           
            justify = tk.LEFT,  
            wraplength=100   
            ).place(x = 300, y = 25, width = 100,height = 100)
        

        
        StandardLabel(
            "Dark_Room_Status",
            root,
            image = TkImage("status_Bad",r"images/Status_Bad.png").image,
                    ).place(x = 150, y = 20)
        

        self.process_display.set("GUI built, initalizing Spectrometer")
        self.load_spec()



    #endregion

    #region spectro init
    def load_spec(self):
        return
            
    
    #endregion

    #region Spectro usage
    def take_dark(self):
        return
    
    def take_data(self):
        return

    #endregion

    #region Data handling
    def save(self):
        '''
        place holder for toggleing graph

        '''

        state = self.graphwindow.state()
        print(state)
        if state == 'normal':
            self.graphwindow.withdraw()

        if state == 'withdrawn':
            self.graphwindow.deiconify()

        





        return
  
    #endregion

if __name__ == "__main__":
    temp = resistain_app()

    temp.startApp()
