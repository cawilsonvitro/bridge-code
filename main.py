#region Imports
import tkinter as tk
from tkinter import Misc
import tkinter.ttk as ttk
import spec_controller as sc
import led_controller as lc
from gui import *
import json
import os
import time 
import numpy as np
import csv
from datetime import datetime as dt
import matplotlib.pyplot as plt



#endregion 

class resistain_app:

    #region Application control
    def __init__(self):
        '''
        intit. class for use
        '''
        self.quit = False
        self.process_display = None

        #spectometer
        self.spectrometer = None
        self.integration_time = None
        self.integration_time_record = None
        self.model = None

        #led 
        self.led_driver = None
        self.current = 2

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

        #movie
        self.light_video = []
        self.timestamps = []
        self.timestart = []
        self.record_time = None

        #data management
        self.startPt = None
        self.stopPt = None
        self.dataPath = r"data/"
        self.videoPath = r"data/Video/"
        self.currentVideoPath = None
        self.sample_num = 1
        self.exst = ".csv"

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
        self.spectrometer.quit()
        self.led_driver.quit()
        
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
            command = self.take_light
        ).place(x = 30,y = 85)
        
        StandardButtons(
                "Record",
                root,
                image = TkImage("Record",r"images/Record.png").image,
                command = self.record
        ).place(x = 30, y = 145)

        

        StandardButtons(
            "Save",
            root,
            image = TkImage("Save", r"images/Save.png").image,
            command = self.save
        ).place(x = 30, y = 205)


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
            ).place(x = 300, y = 200, width = 180,height = 200)
        
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
        self.process_display.set("loading Config")
        if not os.path.isfile('config.json'): #checking if file exists if not making one
            self.process_display.set("Config not found creating Default Config")
            default_spec = {
                "Spectrometer": {
                "integrationtime": "100000",
                "inttime_record": "50000",
                "model": "HR2000PLUS",
                "darkAvgs": "10",
                "lightAvgs": "10",
                "recordtime":"60",
                "BoxCar": "5",
                "startPt":"300",
                "stopPt":"1550"
                            }
                        }
            with open('config.json','w+') as f:
                json.dump(default_spec, f)#if file not found creates file with default configs
        with open('config.json') as f:
            self.config = json.load(f)
            self.spec_config = self.config["Spectrometer"]
        
        self.process_display.set("Config loaded Initalizing Spectrometer")

        self.model = self.spec_config["model"]
        self.integration_time = int(self.spec_config["integrationtime"])
        self.integration_time_record = int(self.spec_config["inttimerecord"])
        self.dark_avg = int(self.spec_config["darkAvgs"])
        self.light_avg = int(self.spec_config["lightAvgs"])
        self.record_time = int(self.spec_config["recordtime"])
        self.boxcar = int(self.spec_config["BoxCar"])
        self.adjust = int(self.boxcar/2)
        self.startPt = int(self.spec_config["startPt"])
        self.stopPt = int(self.spec_config["stopPt"])
        


        try:
            self.spectrometer = sc.oceanoptic_controller(self.integration_time, self.model)
            self.spectrometer.init_spec()
            self.spectrometer.get_spectra()
            if self.spectrometer.status:
                self.process_display.set("Spectrometer Ready")
                self.wl = self.spectrometer.wl
                self.wl_adj = self.wl[self.adjust:-self.adjust]
            else:
                self.process_display.set("No Spectrometer found")
        except Exception as e:
            error = "failed: " + str(e)
            self.process_display.set(error)
        
        finally:
            self.load_led()



    
    #endregion

    #region led init
    def load_led(self):
        self.process_display.set("Loading LED Controller")
        self.root.update_idletasks()
        self.led_driver = lc.dc2200()
        self.led_driver.init_driver()

        if self.led_driver.status: self.process_display.set("LED loaded")
        else: 
            self.process_display.set(self.led_driver.C_error)

    #endregion 

    #region Spectro usage

#need to add led control and error handling.

    def take_dark(self):
        '''
        takes dark sample to normalize against
        '''
        if self.status_check():
            self.process_display.set("taking dark room sample")
            self.root.update_idletasks()
            self.dark = False
            #turning off led
            self.led_driver.off()
            try:
                i = 0 
                dark_temp = 0
                self.dark_intens = 0
                while i < self.dark_avg:
                    self.spectrometer.get_spectra()
                    dark_temp = self.spectrometer.intens
                    self.dark_intens = np.add(self.dark_intens, dark_temp)
                    i += 1
                
                self.dark_intens_avg = self.dark_intens/self.dark_avg
                self.dark_intens_avg = np.convolve(self.dark_intens_avg, np.ones(self.boxcar), 'valid')/self.boxcar

                StandardLabel(
                "Dark_Room_Status",
                self.root,
                image = TkImage("status_Bad",r"images/Status_Good.png").image,
                        ).place(x = 150, y = 20)
                
                self.process_display.set("dark sample completed")
                self.dark = True

            except Exception as e:
                StandardLabel(
                "Dark_Room_Status",
                self.root,
                image = TkImage("status_Bad",r"images/Status_Bad.png").image,
                        ).place(x = 150, y = 20)
                self.process_display.set(e)
        
    def take_light(self):
        '''
        takes light sample sample
        '''

        if self.status_check:
            self.led_driver.on(self.current)
            if not self.dark:
                self.process_display.set(" Please take dark sample first")
            else:
                self.process_display.set("taking light sample")
                self.root.update_idletasks()
                
                try:
                    i = 0
                    light_temp = 0
                    self.light_intens = 0
                    self.spectrometer.get_spectra()
                    while i < self.light_avg:

                        self.spectrometer.get_spectra()
                        light_temp = self.spectrometer.intens
                        self.light_intens = np.add(self.light_intens, light_temp)
                        i += 1
                    #need to add fast graph 
                    self.light_intens_avg = self.light_intens/self.light_avg
                    self.light_intens_avg = np.convolve(self.light_intens_avg, np.ones(self.boxcar), 'valid')/self.boxcar
                    self.process_display.set("Light Sample taken")
                    self.led_driver.off()
                    self.graph()
                    self.process_display.set("light sample completed")
                    self.root.update_idletasks()

                except Exception as e:
                    self.led_driver.off()
                    self.process_display.set(e)

    def record(self):
        '''
        takes multiple frames of data a second
        
        ''' 
        #first make sure we have the right integration time
        
        self.spectrometer.change_int_time(self.integration_time_record)     
        self.spectrometer.get_spectra() #just to make sure we have wl
        self.wl = self.spectrometer.wl
        if self.status_check:
            self.led_driver.on(self.current)
            if not self.dark:
                self.process_display.set("Please take dark sample first")
            else:
                self.process_display.set("Starting recording")
                self.root.update_idletasks()

            try:
                i = 0
                start = time.time()
                end = -1
                while i < self.record_time:
                    self.spectrometer.fast_spectra()
                    self.light_video.append(self.spectrometer.intens)
                    self.timestart.append(
                        dt.now().strftime("%m-%d-%Y, Hour %H Min %M Sec %S") + " " + str(i)
                        )
                    if end == -1:
                        self.timestamps.append(0)
                    else:
                        self.timestamps.append(end-start)
                    i += 1
                    end = time.time()
            except Exception as e:
                self.process_display.set(e)
            
            self.process_display.set("recording finished")
            self.video()
            

    #endregion

    #region Data handling

    def graph(self):
        self.sp = np.subtract(self.light_intens_avg, self.dark_intens_avg)

        
        #getting date and time
        
        self.date = dt.now().strftime("%m/%d/%Y, %H:%M:%S")
        plt.plot(self.wl_adj[self.startPt:self.stopPt],self.sp[self.startPt:self.stopPt])
        plt.ylabel("Intensity")
        plt.xlabel("Wavelength")
        
        plt.title(self.date)
        plt.show()
    
    def get_sample_num(self):
        files = os.listdir(self.dataPath)
        paths = [os.path.join(self.dataPath, basename) for basename in files]
        last_file = max(paths, key=os.path.getctime)
        self.exst = ".csv"

        last_file = last_file[:last_file.find(self.exst)]

        self.date = dt.now().strftime("%m-%d-%Y, Hour %H Min %M Sec %S")
        day = self.date[:self.date.find(",")]

        if last_file.find(day) != -1:
            self.sample_num = str(int(last_file[-1]) + 1)
    
    def save(self):
        try:
            
            
            self.get_sample_num()
            file = self.date + " " + "sample " + self.sample_num + r".csv"
            filepath = self.dataPath + file




            header = ["Wavelength", "Light", "Dark", "Normalized"]
            with open(filepath, "w+", newline = "\n") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                i = 0
                
                for wl in self.wl_adj:
                    row = [wl, 
                            self.light_intens_avg[i],
                            self.dark_intens_avg[i],  
                            self.sp[i]]
                    writer.writerow(row)
                    i += 1
            display = "data saved to : " + filepath
            self.process_display.set(display)
        except AttributeError:
            self.process_display.set("Please take samples first")
            self.root.update_idletasks()
        except Exception as e:
            self.process_display.set(e)
    
    def get_video_num(self):
        #went overboard folders dont need to be in order
        #if dir doesn't exist to hold all videos make one
        if os.path.isdir(self.videoPath):folders = [x[0] for x in os.walk("data")]
        else: os.makedirs(self.videoPath)
        folder_name = dt.now().strftime("%m-%d-%Y")

        current_folders =[x[0] for x in os.walk(self.videoPath)]
        sample_nums = []
        if len(current_folders) <= 1:
            end = "_1"
        else:
            for folder in current_folders[1:]:
                sample_num = int(folder[folder.find("_")+1:])
                sample_nums.append(sample_num)

            end = "_" + str(max(sample_nums) + 1)

        self.currentVideoPath =self.videoPath + folder_name + end
        os.mkdir(self.currentVideoPath)

        self.currentVideoPath += r"/"    
        
    def video(self):
            

            #just displaying max intensity at time t
            max_wls = []
            max_ints = []

            for frame in self.light_video:
                max_int = max(frame)
                max_idx = np.where(frame == max_int)

                max_ints.append(max_int)
                max_wls.append(self.spectrometer.wl[max_idx][0])
            fig, axs = plt.subplots(2,1)

            axs[0].plot(self.timestamps,max_ints)
            axs[0].set_xlabel("Tine [sec]")
            axs[0].set_ylabel("Intensity ")
            axs[1].plot(self.timestamps, max_wls)

            fig.show()
            #add for saving all spectra to folder.
            self.get_video_num()

            i = 0
            self.process_display.set("saving readings")
            header = ["Wavelength","Measurement","Dark"]
            for spectra in self.light_video:
                filepath = self.currentVideoPath + self.timestart[i] + r'.csv'
                with open(filepath, "w+", newline="\n") as f:
                    j = 0
                    writer = csv.writer(f)
                    writer.writerow(header)
                    
                    for wl in self.wl:
                        row = [self.wl[j], self.light_video[i][j], self.dark_intens_avg[i]]
                        writer.writerow(row)
                        j += 1

                i += 1
            self.process_display.set("reading saved")


            



            

    #endregion

    #region error handling
    def status_check(self):
        if self.spectrometer.status and self.led_driver.status:
            return True
        else:
            if not self.spectrometer.status:
                self.load_spec()
            if not self.led_driver.status:
                self.load_led()

    #endregion

if __name__ == "__main__":
    temp = resistain_app()

    temp.startApp()
