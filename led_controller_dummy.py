import ctypes #previous thorlabs controllers I made use 'from ctypes import *' this
#is a bad practice as I need to be extra careful with var names as I could acc. ref something in the ctype lib
import os
import time
import sys


class dc2200(): #this is named this way mainly because it is for a spef device not a general library
    def __init__(self):
        # initalizing all our vars 
        self.status = False
        

    def  init_driver(self):
        '''
        loads the dll to the controller and initializes the dll

        Parameters
        -----------

        Returns
        --------
        None
        '''
        self.status = True

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
        self.cur_error = 0
        self.state = True

    def off(self):
        self.state = False
       
        

    def toggle(self, current = 2):
        if self.state == False: self.on(current)
        if self.state == True: self.off()



    
    def quit(self):
        print("I QUIT")
        # self.lib.TLDC2200_setLedOnOff(self.led_handle, False)
        # self.lib.TLDC2200_close(self.led_handle)





# test = dc2200()

# test.init_driver()
# print(test.status)
# print(test.C_error)
# test.toggle(2)
# print(test.cur_error)
# time.sleep(5)
# test.close()