import ctypes #previous thorlabs controllers I made use 'from ctypes import *' this
#is a bad practice as I need to be extra careful with var names as I could acc. ref something in the ctype lib
import os
import time
import sys


class dc2200(): #this is named this way mainly because it is for a spef device not a general library
    def __init__(self):
        # initalizing all our vars 
        self.libpath = r"C:\Program Files\IVI Foundation\VISA\Win64\Bin" #path to library
        self.lib = None #attribute to hold our loaded library
        self.cwd = os.getcwd() #gets current working director to move back to
        self.status = False #keeps track of if we are connected and working
        self.dll_init = None
        self.func_results = None #stores results from dll  call for error checking
        self.resource_path = b"USB0::0x1313::0x80C8::M01235650::INSTR" #m is just sn or device instance path
        self.led_handle = ctypes.c_int() #devSession in sample
        self.C_error = None
        
        self.cur_error = None #error in applied current to led
        self.current = None #keep track of current requested to led
        self.state = False #keep track of led on or off

    def  init_driver(self):
        '''
        loads the dll to the controller and initializes the dll

        Parameters
        -----------

        Returns
        --------
        None
        '''

        self.status = False
        #os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin") if using 3.7 or newer, not going to waist time making if we should
        #not be using python this old
        os.add_dll_directory(self.libpath)
        self.lib = ctypes.cdll.LoadLibrary("TLDC2200_64.dll")

        self.func_results = self.lib.TLDC2200_init(b"USB0::0x1313::0x80C8::M01235650::INSTR",False,False,ctypes.byref(self.led_handle))

        if self.func_results != 0:
            self.status = False
            errorMessage=ctypes.create_string_buffer(1024)
            self.lib.TLDC2200_error_message(self.led_handle,self.func_results,ctypes.byref(errorMessage))
            self.C_error = errorMessage.value.decode('utf_8')
        else:
            self.status = True

            #make sure we are in constant current
            self.lib.TLDC2200_setOperationMode(self.led_handle, 0)
            #make sure led is off to match state
            self.lib.TLDC2200_setLedOnOff(self.led_handle, False)

    def on(self,current = 2):
        '''
        loads the dll to the controller and initializes the dll

        Parameters
        -----------
        current - led current in Amps
        Returns
        --------
        None
        '''
        self.current = current
        self.state = True
        self.lib.TLDC2200_setConstCurrent(self.led_handle, ctypes.c_float(self.current))
        self.lib.TLDC2200_setLedOnOff(self.led_handle, self.state)
        time.sleep(1) #need to give intrument time to get results
        #check if current is acc.
        applied_current_handle = ctypes.c_double()
        self.lib.TLDC2200_get_led_current_measurement(self.led_handle, ctypes.byref(applied_current_handle))
        app_curr = float(applied_current_handle.value)
        self.cur_error = 100 * abs((app_curr - self.current)/self.current)


    def off(self):
        self.state = False
        self.lib.TLDC2200_setLedOnOff(self.led_handle, self.state)
        

    def toggle(self, current):
        if self.state == False: self.on(current)
        if self.state == True: self.off()



    
    def quit(self):
        self.lib.TLDC2200_setLedOnOff(self.led_handle, False)
        self.lib.TLDC2200_close(self.led_handle)





# test = dc2200()

# test.init_driver()
# print(test.status)
# print(test.C_error)
# test.toggle(2)
# print(test.cur_error)
# time.sleep(5)
# test.close()