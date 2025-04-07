import os
import time
import matplotlib.pyplot as plt
from ctypes import *
# from infi.devicemanager import DeviceManager
import csv
import datetime as dt




class css_controller():

    def __init__(self, integration_time: float):

        # initalizing all our vars 
        self.libpath = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin" #path to library
        self.lib = None #attribute to hold our loaded library
        self.results = None #holds results to be saved in csv file
        self.cwd = os.getcwd() #gets current working director to move back to
        
        
        self.dll_init = None
        self.ccs_handle = c_int(0)
        self.func_results = None #stores results from dll  call for error checking
        self.resource_path = b"USB0::0x1313::0x8089::M01068544::RAW" #m is just sn or device instance path
        self.integration_time = c_double(integration_time)
        self.status = False #keeps track of if we are connected and working 
        self.intens = (c_double*3648)() #stores the intens
        self.wavelengths = (c_double*3648)() #stors wavelenght

        self.thorspectra_error = -1073807246 #if thorSpectra is open this will be the error
        

    
    def init_spec(self):
        '''
        loads the dll to the controller and initializes the dll

        Parameters
        -----------

        Returns
        --------
        None
        '''
        self.status = False
        os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
        self.lib = cdll.LoadLibrary("TLCCS_64")
        os.chdir(self.cwd)
        self.func_results = self.lib.tlccs_init(self.resource_path, 1, 1, byref(self.ccs_handle))
        print(self.func_results)
        if self.func_results != 0: #if we are good to go this function should return 0, here we are checking that
            self.status = False
            print("error occured while initalized dll", self.func_results)
        if self.func_results == self.thorspectra_error:
            self.status = False
            print("Please make sure the ThorSpectra software is closed")
        if self.func_results == 0:
            self.status = True

        self.func_results = self.lib.tlccs_getDeviceStatus(self.resource_path, c_int32(0))
        
    def get_spectra(self):
        '''
        runs a scan using the css devices 
        '''


        if not self.status:
            print("no css device connected attempting to find")
            self.init_spec()

        if self.status:
            self.lib.tlccs_getWavelengthData(self.ccs_handle, 0, byref(self.wavelengths), c_void_p(None), c_void_p(None))
            self.lib.tlccs_getScanData(self.ccs_handle, byref(self.intens))
            plt.plot(self.wavelengths,self.intens)
            plt.show()
            

# test = css_controller(.212)
# # test.windows_check()
# test.load_cdll()
# # test.status = True
# test.get_spectra()
