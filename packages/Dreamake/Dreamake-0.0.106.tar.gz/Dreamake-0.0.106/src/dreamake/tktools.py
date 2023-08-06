from tkinter.filedialog import *
from tkinter.colorchooser import *
from tkinter import Tk


def ask_color():
    root = Tk()
    root.withdraw()
    color = askcolor()[0]
    root.destroy()
    return color