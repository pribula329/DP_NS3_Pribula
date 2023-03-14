from tkinter import filedialog
from api import saxParser
from api import visualisation
from GUI import gui
path = ""
speed = 1.0
line_id = "null"
simulationOnOff = True
count_iteration = 0
max_iteration = 0
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
    global max_iteration
    max_iteration = saxParser.handler.transportCount
    gui.stepLabel.config(text="Steps: "+ str(count_iteration)+"/"+str(max_iteration))
    visualisation.create_node(board=gui.board, handler=saxParser.handler)


def start_simulation():
    """
        Function for start simulation
    """
    global simulationOnOff
    global line_id
    global count_iteration
    count_iteration = 0
    simulationOnOff = True
    #visualization comunication
    visualisation.create_transport_line(board=gui.board, handler=saxParser.handler, iteration=count_iteration)

def pause_simulation():
    global simulationOnOff
    simulationOnOff = False


def resume_simulation():
    global simulationOnOff
    simulationOnOff = True
    print(count_iteration)
    visualisation.create_transport_line(board=gui.board, handler=saxParser.handler, iteration=count_iteration)


def forward_simulation():
    visualisation.create_step_line(board=gui.board, handler=saxParser.handler, iteration=count_iteration, step="f")


def back_simulation():
    visualisation.create_step_line(board=gui.board, handler=saxParser.handler, iteration=count_iteration, step="b")


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

