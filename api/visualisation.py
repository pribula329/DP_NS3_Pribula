import time

from time_profiler import timer
from memory_profiler import profile

from api import function
from api import saxParser
import tkinter as tk
from time import sleep
from GUI import move
from GUI import zoom
from GUI import gui
import asyncio

MAX = 5.0
COUNT_TIME = 0
DELETE_ON_OFF = True
SLEEP_COUNT = 0.0
DELAY_SLEEP=0.0
def create_node(board, handler):
    """
    Function for draw nodes to board
    :param board: Tkinter board
    :param handler: Sax parser handler with data
    """
    global COUNT_TIME
    COUNT_TIME = 0
    for i in handler.node:
        # +MAX for biggest size
        coord = float(i[2]), float(i[3]), float(i[2])+MAX, float(i[3])+MAX
        #(type(coord[0]))

        y = list(coord)
        for c in range(len(y)):
            #print(y[c])
            y[c] = y[c]*MAX
        coord = tuple(y)

        #print(type(coord[0]))


        id_node = board.create_oval(coord, fill="blue")

        #/2 for input ID to node
        id_text = board.create_text(float((coord[0]+coord[2])/2.0), float((coord[1]+coord[3])/2.0), text=handler.nodeDesc[str(i[0])], fill="white")
        function.node_id.update({i[0] : [id_node, id_text]})

        # move board
        board.bind("<ButtonPress-1>", lambda event: move.move_start(event, board))
        board.bind("<B1-Motion>", lambda event: move.move_move(event, board))

        board.bind("<ButtonPress-2>", lambda event: move.pressed2(event, board))
        # board.bind("<Motion>", lambda event: move.move_move2(event, board))
        board.update()

@timer()
@profile
def create_transport_line(board, handler, iteration):
    """
    Function for draw line between 2 nodes
    :param board: Tkinter board
    :param handler: Sax parser handler with data
    """

    #line_id = "null"

    #print(function.simulationOnOff)
    for t in handler.transport[iteration:]:
        if not function.simulationOnOff:
            break


        helper_update(handler)

        global DELETE_ON_OFF
        DELETE_ON_OFF = True
        call_async(board)
        #print(function.count_iteration)
        gui_update(handler=handler)

        function.count_iteration = function.count_iteration + 1
        #check change position
        if function.count_iteration in handler.nodeChangePos:
            new_node_create(board, handler, function.count_iteration)

        if not check_transport(handler=handler,iteration=function.count_iteration-1,iterationNext=function.count_iteration):
            first, last = t[0], t[1]
            coordFirst = handler.node[int(first)].copy()
            color = 'green'
            if last == "-":

                coordLast = handler.node[int(first)].copy()
                coordLast[3] = coordLast[3] + 5
                color = 'red'

            else:
                coordLast = handler.node[int(last)].copy()



            # print("scale",zoom.scale)
            #board.create_line((coordFirst[2] + 2.5) * zoom.scale, (coordFirst[3] + 2.5) * zoom.scale,
            #                  (coordLast[2] + 2.5) * zoom.scale, (coordLast[3] + 2.5) * zoom.scale, arrow=tk.LAST)

            #### append time of line which send data


            new_line_id = board.create_line((coordFirst[2] + 2.5) * MAX, (coordFirst[3] + 2.5) * MAX,
                                                 (coordLast[2] + 2.5) * MAX, (coordLast[3] + 2.5) * MAX, arrow=tk.LAST,
                                                 width=3, fill=color)

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
            if len(function.help_time_line_array)>1:
                function.help_time_line_array.pop(len(function.help_time_line_array)-2)

        try:
            if (float(function.help_time_line_array[-1])) - (time.time() - function.t1_start - SLEEP_COUNT)>0:
            #print((float(function.help_time_line_array[-1])) - (time.time() - function.t1_start - SLEEP_COUNT))

                sleep(float(function.help_time_line_array[-1]) - (time.time() - function.t1_start - SLEEP_COUNT))
        except:
                #print("nestihol spat")
            None
        #board.after(int(function.speed*1000),board.update())

        if function.count_iteration%150==0:
            board.update()
        #sleep(function.speed)
    t1_stop = time.time()


    #print("Elapsed time during the whole program in seconds:",
     #     t1_stop - function.t1_start)
    board.update()


async def call(board):
    await asyncio.gather(time_line_delete(), delete_line(board))
def call_async(board):

    loop = asyncio.get_event_loop()
    loop.run_until_complete(call(board))
async def time_line_delete():
    global COUNT_TIME
    global DELETE_ON_OFF
    global SLEEP_COUNT
    if len(function.time_line_array) > 1:
        #print(function.time_line_array[COUNT_TIME+1])
        #print(function.time_line_array[COUNT_TIME])
        #print(float(function.time_line_array[COUNT_TIME+1]) - float(function.time_line_array[COUNT_TIME]))
        #print(abs(float(function.time_line_array[COUNT_TIME+1]) - float(function.time_line_array[COUNT_TIME])))
        sleep_time = float(function.time_line_array[COUNT_TIME+1]) - float(function.time_line_array[COUNT_TIME])

        if sleep_time > 0:

            #print("Sleep Time: " + str(sleep_time+function.speed))
            SLEEP_COUNT += function.speed
            await asyncio.sleep(sleep_time+function.speed)
        else:
            await asyncio.sleep(0)
        COUNT_TIME = COUNT_TIME + 1
    DELETE_ON_OFF = False

async def delete_line(board):

    while DELETE_ON_OFF:

        #print("Time")
        #print(time.time() - function.t1_start - function.speed)
        #print("Delay")

        #print(function.help_time_line_array)
        #print("Pocet casov: " + str(len(function.line_id_array)))
        try:
            #print(time.time() - function.t1_start - SLEEP_COUNT - (float(function.help_time_line_array[0])))
            while ((time.time() - function.t1_start - SLEEP_COUNT) - (float(function.help_time_line_array[0]))) >= 0.5:

                function.help_time_line_array.pop(0)
                board.delete(function.line_id_array[0])
                function.line_id_array.pop(0)


                #print("pocet casov: " + str(len(function.help_time_line_array)))
                #print("pocet ciar: " + str(len(function.line_id_array)))
            board.update()

        except:
            #print("ziadne ciary a casy zatial")
            None
        await asyncio.sleep(0)





def create_step_line(board, handler, iteration, step):
    delete_all(board)

    check = False
    color = 'green'
    trans = []
    if step=="f":
        trans = handler.transport[iteration]
        function.count_iteration = function.count_iteration + 1


    if step=="b":
        trans = handler.transport[iteration - 2]
        function.count_iteration = function.count_iteration - 1


    first, last = trans[0], trans[1]
    coordFirst = handler.node[int(first)].copy()

    if last == "-":
        coordLast = handler.node[int(first)].copy()
        coordLast[3] = coordLast[3] + 5
        color = 'red'

    else:
        coordLast = handler.node[int(last)].copy()

    gui_update(handler=handler)

    # check change position
    if function.count_iteration in handler.nodeChangePos:
        new_node_create(board, handler, function.count_iteration)



    if function.line_id != "null":
        board.delete(function.line_id)

    function.line_id = board.create_line((coordFirst[2] + 2.5) * MAX, (coordFirst[3] + 2.5) * MAX,
                                        (coordLast[2] + 2.5) * MAX, (coordLast[3] + 2.5) * MAX, arrow=tk.LAST, width=3,
                                        fill=color)
        # line_id = board.create_line((coordFirst[2] + 2.5), (coordFirst[3] + 2.5),
        #                  (coordLast[2] + 2.5), (coordLast[3] + 2.5), arrow=tk.LAST)

    board.update()






def check_transport(handler, iteration, iterationNext):
    try:

        trans = handler.transport[iteration].copy()
        transNext = handler.transport[iterationNext].copy()

        if trans == transNext:

            return True
        else:
            return False
    except:
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
            #print(type(coord[0]))
            ###only for max point later DELETE
            y = list(coord)
            for c in range(len(y)):
                #print(y[c])
                y[c] = y[c] * MAX
            coord = tuple(y)

            #print(type(coord[0]))


            id_node = board.create_oval(coord, fill="blue")
            # /2 for input ID to node
            id_text = board.create_text(float((coord[0] + coord[2]) / 2.0), float((coord[1] + coord[3]) / 2.0),
                                        text=handler.nodeDesc[str(x[0])], fill="white")
            function.node_id.update({x[0]: [id_node, id_text]})



def gui_update(handler):
    gui.stepLabel.config(text="Steps: " + str(function.count_iteration+1) + "/" + str(function.max_iteration))
    gui.textLabel.delete('1.0', tk.END)
    gui.textLabel.insert(tk.END, handler.metaInfo[function.count_iteration])
    gui.timeLabel.config(text="Time: " + handler.transportTime[function.count_iteration] + " s")

def helper_update(handler):
    function.time_line_array.append(handler.transportTime[function.count_iteration])
    function.help_time_line_array.append(handler.transportTime[function.count_iteration])


def delete_all(board):
    for x in function.line_id_array:
        board.delete(x)
    function.time_line_array = []
