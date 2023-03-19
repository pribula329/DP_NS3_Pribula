import tkinter
from GUI import gui

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("1080x750")
    root.title("Vizualizer NS3")
    gui.create_gui(root)

    tkinter.mainloop()


