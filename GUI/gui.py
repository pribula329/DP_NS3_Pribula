import tkinter as tk
from tkinter.ttk import *
from api import function


board
simulationOnOff


def create_gui(gui):
    """
    Function for create GUI
    :param gui: Tkinter root widget  screen
    """
    global board
    global simulationOnOff

    board = tk.Canvas(gui, background="white", height=650, width=800)
    board.grid(row=2,columnspan=3)

    # button widget
    b1 = Button(gui, text="Load", command=function.open_file)
    b2 = Button(gui, text="Start", command=function.start_simulation)
    b3 = Button(gui, text="Pause", command=function.start_simulation)
    # arranging button widgets
    b1.grid(row=0, column=0)
    b2.grid(row=0, column=1)
    b3.grid(row=0, column=2)

    l1 = Label(gui, text="Slow")
    l1.grid(row=0, column=3)
    varScale = tk.DoubleVar()
    s1 = tk.Scale(gui, from_=0.0, to=2.0, orient="horizontal", resolution=0.10,
               command=function.change_speed, variable=varScale)
    s1.set(1.0)
    s1.grid(row=0, column=4)

    l2 = Label(gui, text="Fast")
    l2.grid(row=0, column=5)




