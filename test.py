# # import random
# # import tkinter as Tk
# # from itertools import count

# # import matplotlib.pyplot as plt
# # from matplotlib.animation import FuncAnimation
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # import spec_controller as sc
# # import time

# # plt.style.use('fivethirtyeight')
# # # values for first graph
# # x_vals = []
# # y_vals = []


# # index = count()
# # index2 = count()

# # spectrometer = sc.oceanoptic_controller(50000, "HR2000PLUS")





# import matplotlib.pyplot as plt


# x = range(0,5)
# y = range(0,5)

# plt.plot(x,y)
# plt.show()
# from datetime import datetime as dt


# print(len(dt.now().strftime("%H:%M:%S.%f")))

# import time


# print(time.time())


# import os

# test = os.walk(r"data")

# for x in test:
#     print(x[0])

# end = True

# print(os.path.isdir(r"data\Videos"))

# from datetime import datetime as dt

# a = [1,2,3]
# print(max(a))

# folder = "data/Video/"



# print(folder[folder.find("_"):])

import matplotlib.pyplot as plt
data = [1,3,2,8,10,0,9]
data2 = [300,500,700,300,600,700,000]
fig, axs = plt.subplots(2,1)
axs[0].plot(data)
axs[1].plot(data2)
# cb = axs[1].pcolormesh([data2]*2, cmap='hot', shading='gouraud')
# fig.colorbar(cb, ax = axs[1])
fig.show()

dsaf = 1