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


        id_node = board.create_oval(coord, fill="red")
        #/2 for input ID to node
        id_text = board.create_text(float((coord[0]+coord[2])/2.0), float((coord[1]+coord[3])/2.0), text=handler.nodeDesc[str(i[0])], fill="white")
        function.node_id.update({i[0] : [id_node, id_text]})
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
        gui_update(handler=handler)

        #check change position
        if function.count_iteration in [517,520,523,529,532,538]:
            new_node_create(board, handler, function.count_iteration)

        if not check_transport(handler=handler,iteration=function.count_iteration,iterationNext=function.count_iteration+1):
            first, last = t[0], t[1]
            # print(first)
            coordFirst = handler.node[first]
            coordLast = handler.node[last]
            # print("scale",zoom.scale)
            #board.create_line((coordFirst[2] + 2.5) * zoom.scale, (coordFirst[3] + 2.5) * zoom.scale,
            #                  (coordLast[2] + 2.5) * zoom.scale, (coordLast[3] + 2.5) * zoom.scale, arrow=tk.LAST)

            #### append time of line which send data


            new_line_id = board.create_line((coordFirst[2] + 2.5) * MAX, (coordFirst[3] + 2.5) * MAX,
                                                 (coordLast[2] + 2.5) * MAX, (coordLast[3] + 2.5) * MAX, arrow=tk.LAST,
                                                 width=3, fill='green')

            function.line_id_array.append(new_line_id)



            ### step by step
            #if function.line_id != "null":
            #    board.delete(function.line_id)
            #
            #function.line_id = board.create_line((coordFirst[2] + 2.5)*MAX, (coordFirst[3] + 2.5)*MAX,
            #                            (coordLast[2] + 2.5)*MAX, (coordLast[3] + 2.5)*MAX, arrow=tk.LAST, width=3, fill='green')
            #
            #
        else:
            function.time_line_array.pop(len(function.time_line_array)-2)


        time_line_delete(board)


        #board.after(int(function.speed*1000),board.update())



        board.update()
        #sleep(function.speed)


def time_line_delete(board):
    if len(function.time_line_array) > 1:
        sleep(float(function.time_line_array[1]) - float(function.time_line_array[0]) + function.speed)

    if (float(function.time_line_array[-1]) - float(function.time_line_array[0])) >= 1:
        while (float(function.time_line_array[-1]) - float(function.time_line_array[0])) >= 1:
            function.time_line_array.pop(0)
            board.delete(function.line_id_array[0])
            function.line_id_array.pop(0)
            print("pocet casov: " + str(len(function.time_line_array)))
            print("pocet ciar: " + str(len(function.line_id_array)))


def create_step_line(board, handler, iteration, step):
    delete_all(board)

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

    gui_update(handler=handler)

    if not check:

        if function.line_id != "null":
            board.delete(function.line_id)

        function.line_id = board.create_line((coordFirst[2] + 2.5) * MAX, (coordFirst[3] + 2.5) * MAX,
                                             (coordLast[2] + 2.5) * MAX, (coordLast[3] + 2.5) * MAX, arrow=tk.LAST, width=3,
                                             fill='green')
        # line_id = board.create_line((coordFirst[2] + 2.5), (coordFirst[3] + 2.5),
        #                  (coordLast[2] + 2.5), (coordLast[3] + 2.5), arrow=tk.LAST)

    board.update()






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

def new_node_create(board, handler, iteration):
    for x in handler.nodePos:
        if x[3]==iteration:
            #delete node
            deleteNode= function.node_id.get(x[0])
            board.delete(deleteNode[0])
            board.delete(deleteNode[1])

            #create new node

            handler.node[x[0]][2] = x[1]
            handler.node[x[0]][3] = x[2]
            node = handler.node[x[0]]
            coord = float(node[2]), float(node[3]), float(node[2]) + MAX, float(node[3]) + MAX
            print(type(coord[0]))
            ###only for max point later DELETE
            y = list(coord)
            for c in range(len(y)):
                print(y[c])
                y[c] = y[c] * MAX
            coord = tuple(y)

            print(type(coord[0]))


            id_node = board.create_oval(coord, fill="red")
            # /2 for input ID to node
            id_text = board.create_text(float((coord[0] + coord[2]) / 2.0), float((coord[1] + coord[3]) / 2.0),
                                        text=handler.nodeDesc[str(x[0])], fill="white")
            function.node_id.update({x[0]: [id_node, id_text]})



def gui_update(handler):
    gui.stepLabel.config(text="Steps: " + str(function.count_iteration) + "/" + str(function.max_iteration))
    gui.textLabel.delete('1.0', tk.END)
    gui.textLabel.insert(tk.END, handler.metaInfo[function.count_iteration - 1])
    gui.timeLabel.config(text="Time: " + handler.transportTime[function.count_iteration - 1] + " s")
    function.time_line_array.append(handler.transportTime[function.count_iteration - 1])

def delete_all(board):
    for x in function.line_id_array:
        board.delete(x)
    function.time_line_array = []