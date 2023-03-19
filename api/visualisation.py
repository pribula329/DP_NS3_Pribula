from api import function
from api import saxParser
import tkinter as tk
from time import sleep
from GUI import move
from GUI import zoom
from GUI import gui
MAX = 5.0


def create_node(board, handler):
    """
    Function for draw nodes to board
    :param board: Tkinter board
    :param handler: Sax parser handler with data
    """
    for i in handler.node:
        #+5 for biggest size
        coord = float(i[2]), float(i[3]), float(i[2])+MAX, float(i[3])+MAX
        print(type(coord[0]))
        ###only for max point later DELETE
        y = list(coord)
        for c in range(len(y)):
            print(y[c])
            y[c] = y[c]*MAX
        coord = tuple(y)

        print(type(coord[0]))


        board.create_oval(coord, fill="red")
        #/2 for input ID to node
        board.create_text(float((coord[0]+coord[2])/2.0), float((coord[1]+coord[3])/2.0), text=i[0], fill="white")

        # move board
        board.bind("<ButtonPress-1>", lambda event: move.move_start(event, board))
        board.bind("<B1-Motion>", lambda event: move.move_move(event, board))

        board.bind("<ButtonPress-2>", lambda event: move.pressed2(event, board))
        board.bind("<Motion>", lambda event: move.move_move2(event, board))
        board.update()


def create_transport_line(board, handler, iteration):
    """
    Function for draw line between 2 nodes
    :param board: Tkinter board
    :param handler: Sax parser handler with data
    """



    # todo ZOOM
    # windows scroll
    #board.bind("<MouseWheel>", lambda event: zoom.zoomer(event, board))

    #line_id = "null"
    print(function.simulationOnOff)
    for t in handler.transport[iteration:]:
        if not function.simulationOnOff:
            break

        function.count_iteration = function.count_iteration + 1
        print(function.count_iteration)
        gui.stepLabel.config(text="Steps: " + str(function.count_iteration) + "/" + str(function.max_iteration))
        if not check_transport(handler=handler,iteration=function.count_iteration,iterationNext=function.count_iteration+1):
            first, last = t[0], t[1]
            # print(first)
            coordFirst = handler.node[first]
            coordLast = handler.node[last]
            # print("scale",zoom.scale)
            #board.create_line((coordFirst[2] + 2.5) * zoom.scale, (coordFirst[3] + 2.5) * zoom.scale,
            #                  (coordLast[2] + 2.5) * zoom.scale, (coordLast[3] + 2.5) * zoom.scale, arrow=tk.LAST)
            if function.line_id != "null":
                board.delete(function.line_id)

            function.line_id = board.create_line((coordFirst[2] + 2.5)*MAX, (coordFirst[3] + 2.5)*MAX,
                                        (coordLast[2] + 2.5)*MAX, (coordLast[3] + 2.5)*MAX, arrow=tk.LAST, width=3, fill='green')
            #line_id = board.create_line((coordFirst[2] + 2.5), (coordFirst[3] + 2.5),
            #                  (coordLast[2] + 2.5), (coordLast[3] + 2.5), arrow=tk.LAST)



        board.after(int(function.speed*1000),board.update())



        #board.update()
        #sleep(function.speed)


def create_step_line(board, handler, iteration, step):
    check = False
    if step=="f":
        check = check_transport(handler=handler, iteration=function.count_iteration, iterationNext=function.count_iteration + 1)
        trans = handler.transport[iteration+1]
        first, last = trans[0], trans[1]
        # print(first)
        coordFirst = handler.node[first]
        coordLast = handler.node[last]
        function.count_iteration = function.count_iteration + 1


    if step=="b":
        check = check_transport(handler=handler, iteration=function.count_iteration, iterationNext=function.count_iteration - 1)
        trans = handler.transport[iteration - 1]
        first, last = trans[0], trans[1]
        # print(first)
        coordFirst = handler.node[first]
        coordLast = handler.node[last]
        function.count_iteration = function.count_iteration - 1

    gui.stepLabel.config(text="Steps: " + str(function.count_iteration) + "/" + str(function.max_iteration))
    if not check:

        if function.line_id != "null":
            board.delete(function.line_id)

        function.line_id = board.create_line((coordFirst[2] + 2.5) * MAX, (coordFirst[3] + 2.5) * MAX,
                                             (coordLast[2] + 2.5) * MAX, (coordLast[3] + 2.5) * MAX, arrow=tk.LAST, width=3,
                                             fill='green')
        # line_id = board.create_line((coordFirst[2] + 2.5), (coordFirst[3] + 2.5),
        #                  (coordLast[2] + 2.5), (coordLast[3] + 2.5), arrow=tk.LAST)

    board.after(int(function.speed * 1000), board.update())




def check_transport(handler, iteration, iterationNext):
    trans = handler.transport[iteration]
    transNext = handler.transport[iterationNext]
    print(trans)
    print(transNext)
    if trans==transNext:
        print("su rovnake")
        return True
    else:
        print("su ine")
        return False
