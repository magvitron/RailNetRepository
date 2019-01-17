######################################
# seatNumSel.py
######################################
#dependency:  uizero, Tkinter main.py
#
######################################
import os
import time
from guizero import *

app = App(title="SeatSel", width=1024,height=600, layout="grid")
app.tk.overrideredirect(True)
app.tk.geometry("{0}x{1}+0+0".format(app.tk.winfo_screenwidth(), app.tk.winfo_screenheight()))
app.tk.resizable(width=0, height=0)
app.tk.protocol('WM_DELETE_WINDOW','donothing')
app.tk.wm_attributes('-type', 'splash')
app.tk.wm_attributes('-fullscreen','true')
