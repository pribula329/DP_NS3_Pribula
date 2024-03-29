import tkinter as tk
from tkinter.ttk import *
from api import function


global board
#global my_string_var
global stepLabel
global textLabel
global timeLabel
global mylist
def create_gui(gui):
    """
    Function for create GUI
    :param gui: Tkinter root widget  screen
    """
    global board
    board = tk.Canvas(gui, background="white", height=650, width=800)
    board.grid(row=2,rowspan=10, columnspan=4)

    # button widget
    b1 = Button(gui, text="Load", command=function.open_file)
    b2 = Button(gui, text="Start", command=function.start_simulation)
    b3 = Button(gui, text="Pause", command=function.pause_simulation)
    b4 = Button(gui, text="Resume", command=function.resume_simulation)
    b5 = Button(gui, text="Step back", command=function.back_simulation)
    b6 = Button(gui, text="Step forward", command=function.forward_simulation)
    # arranging button widgets
    b1.grid(row=0, column=0)
    b2.grid(row=0, column=1)
    b3.grid(row=0, column=2)
    b4.grid(row=0, column=3)
    b5.grid(row=2, column=5)
    b6.grid(row=2, column=6)

    # scale widget
    l1 = Label(gui, text="Slow")
    l1.grid(row=0, column=5)
    varScale = tk.DoubleVar()
    s1 = tk.Scale(gui, from_=0.0, to=1.0, orient="horizontal", resolution=0.10,
                  command=function.change_speed, variable=varScale)
    s1.set(1.0)
    s1.grid(row=1, column=5, columnspan=2, rowspan=1)

    l2 = Label(gui, text="Fast")
    l2.grid(row=0, column=6)

    #global my_string_var
    global stepLabel
    # create a StringVar class
    my_string_var = tk.StringVar()

    # set the text
    my_string_var.set("Step: 0/0")

    print(my_string_var)
    # create a label widget
    stepLabel = Label(gui, text=my_string_var.get())
    stepLabel.grid(row=3, column=5)

    # global my_string_var
    global timeLabel
    # create a StringVar class
    my_time_var = tk.StringVar()

    # set the text
    my_time_var.set("Time: 0s")

    # create a label widget
    timeLabel = Label(gui, text=my_time_var.get())
    timeLabel.grid(row=4, column=5)

    global textLabel
    # create a StringVar class
    my_text_var = tk.StringVar()

    # set the text
    my_text_var.set("Meta-info")

    textLabel = tk.Text(gui, width=35, height=15)
    textLabel.grid(row=5,column=5,columnspan=2)
    textLabel.insert(tk.END,my_text_var.get())

    #listbox ip Address
    # Set the Menu initially
    scrollMenu = tk.Scrollbar(gui, command=function.start_simulation)

    scrollMenu.grid(row=6,column=5)
    global mylist
    mylist = tk.Listbox(gui, yscrollcommand=scrollMenu.set, height=10, width=30)

    mylist.grid(row=6,column=5)

    scrollMenu.config(command=mylist.yview)






