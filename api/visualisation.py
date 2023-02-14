from api import function
from api import saxParser
import tkinter as tk
from time import sleep
from GUI import move
from GUI import zoom

MAX = 5.0


def create_node(board, handler):
    """
    Function for draw nodes to board
    :param board: Tkinter board
    :param handler: Sax parser handler with data
    """
    for i in handler.node:
        #+5 for biggest size
        coord = float(i[2]), float(i[3]), float(i[2])+5, float(i[3])+5
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


def create_transport_line(board, handler):
    """
    Function for draw line between 2 nodes
    :param board: Tkinter board
    :param handler: Sax parser handler with data
    """

    global line_id
    global simulationOnOff

    # move board
    board.bind("<ButtonPress-1>", lambda event: move.move_start(event, board))
    board.bind("<B1-Motion>", lambda event: move.move_move(event, board))

    board.bind("<ButtonPress-2>", lambda event: move.pressed2(event, board))
    board.bind("<Motion>", lambda event: move.move_move2(event, board))
    # todo ZOOM
    # windows scroll
    #board.bind("<MouseWheel>", lambda event: zoom.zoomer(event, board))
    i = 0
    #line_id = "null"
    for t in handler.transport:
        if simulationOnOff == False:
            break

        first, last = t[0], t[1]
        # print(first)
        coordFirst = handler.node[first]
        coordLast = handler.node[last]
        # print("scale",zoom.scale)
        #board.create_line((coordFirst[2] + 2.5) * zoom.scale, (coordFirst[3] + 2.5) * zoom.scale,
        #                  (coordLast[2] + 2.5) * zoom.scale, (coordLast[3] + 2.5) * zoom.scale, arrow=tk.LAST)
        if line_id != "null":
            board.delete(line_id)

        line_id = board.create_line((coordFirst[2] + 2.5)*MAX, (coordFirst[3] + 2.5)*MAX,
                                    (coordLast[2] + 2.5)*MAX, (coordLast[3] + 2.5)*MAX, arrow=tk.LAST, width=3, fill='green')
        #line_id = board.create_line((coordFirst[2] + 2.5), (coordFirst[3] + 2.5),
        #                  (coordLast[2] + 2.5), (coordLast[3] + 2.5), arrow=tk.LAST)
        board.update()
        sleep(function.speed)
        i += 1
        print(i)
