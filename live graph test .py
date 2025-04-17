import random
import tkinter as Tk
from itertools import count

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import spec_controller as sc
import time

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []


index = count()
index2 = count()

spectrometer = sc.oceanoptic_controller(50000, "HR2000PLUS")
spectrometer.init_spec()

spectrometer.get_spectra()

print(spectrometer.wl)
def animate(i):
    # Generate values    spectrometer.fast_spectra()
    x_vals = spectrometer.wl
    y_vals = spectrometer.intens

    ax1 = plt.gcf().get_axes()[0]
    # Clear current data
    ax1.cla()
    # Plot new data
    ax1.plot(x_vals, y_vals)



# GUI
root = Tk.Tk()
label = Tk.Label(root, text="Realtime Animated Graphs").grid(column=0, row=0)
root.bind("<Escape>", spectrometer.quit())
#graph 
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().grid(column=0, row=1)
#Create one subplot
plt.gcf().subplots(1, 1)
ani = FuncAnimation(plt.gcf(), animate, interval=2000)

Tk.mainloop()



