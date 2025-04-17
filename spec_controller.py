from seabreeze.spectrometers import list_devices, Spectrometer
import datetime as dt


class oceanoptic_controller():
    def __init__(self, integration = 100000, model = 'HR2000PLUS'):
        '''
        init the class 

        Parameters
        -----------
        init_time - integration time of the spectrometer, 

        model - model of the spectrometer

        Returns
        --------
        None
        '''
        self.integration_time = integration
        self.model = model
        self.status = False
        self.wl = []
        self.intens = []
        self.spec = []
        self.error = None
        return
    
    def init_spec(self):
        '''
        loads the dll to the controller and initializes the dll using model name to find correct ocean optics spectr.

        Parameters
        -----------

        Returns
        --------
        None
        '''
        try:
            devices = list_devices()
            if len(devices) == 0:
                self.status = False
            else:
                # self.spec = Spectrometer.from_first_available()
                # self.spec.integration_time_micros(self.integration_time)
                # self.status = True
                i = 0
                found = False
                for device in devices:
                    if device.model == self.model:
                        found = True
                        break
                    i += 1
                if found != False:
                    self.spec = Spectrometer.from_serial_number(devices[i].serial_number)
                    self.spec.integration_time_micros(self.integration_time)
                    self.status = True
                else:
                    print("wrong spectrometer name found please select from below list and add to the model section in config.json")
                    for device in devices:
                        print(device.model)
                    self.status = False
        except Exception as e:
            self.error = e
        return 


    def get_spectra(self):
        try:
            if not self.status:
                print("Ocean optics device not found attempting to find ")
                self.init_spec()
            else:
                self.wl = self.spec.wavelengths()
                self.intens = self.spec.intensities()
        except:
            self.status = False

    def fast_spectra(self):
        '''
        directly calls the function to get spectrometer intensity without any error handling
        to speed it up. Also does not get wavelengths

        Parameters
        -----------

        Returns
        --------
        None
        '''
        self.intens = self.spec.intensities()
    
    def change_int_time(self,int_time):
        '''
        wrapper for chaning integration time

        Parameters
        -----------

        Returns
        --------
        None
        '''
        self.spec.integration_time_micros(int(int_time))

    
    def quit(self):
        self.spec.close()
        

# test = oceanoptic_controller(integration = 212000,model='USB2000PLUS')


# test.init_spec()

# test.get_spectra()

# print(test.wl)

# test.quit()