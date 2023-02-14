from tkinter import filedialog
from api import saxParser
from api import visualisation
from GUI import gui
path = ""
speed = 1.0

def open_file():
    """
        Function for open file and draw nodes on board
    """
    global path
    path = filedialog.askopenfilename(
        filetypes=[("SEM readable files", (".xml")), ("SEM XML files", ("*.xml", ".sem")), ("All files", ".*")])
    saxParser.read_sax_parser(path)
    # visualiztion node
    gui.board.delete("all")
    visualisation.create_node(board=gui.board, handler=saxParser.handler)


def start_simulation():
    """
        Function for start simulation
    """
    global simulationOnOff
    global line_id
    line_id = "null"
    simulationOnOff = True
    #visualization comunication
    visualisation.create_transport_line(board=gui.board, handler=saxParser.handler)

def pause_simulation():
    global simulationOnOff
    simulationOnOff = False

def change_speed(varScaleSpeed):
    """
        Function for change speed of simulation
        :param varScaleSpeed: Value of speed from user
    """
    global speed
    if float(varScaleSpeed)>1:
        speed = 2.05 - float(varScaleSpeed)
    else:
        speed = 1.0 + float(varScaleSpeed)

    print(speed)

