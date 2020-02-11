from pyfirmata.util import Iterator 
import pyfirmata
import time
import zmq
import os

class Setting:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def return_list(self):
        return [self.name, self.value]

    def __str__(self):
        return (self.name + "#" + self.value) 

def import_arduino(COM1 = "COM3", COM2 = "COM4"):
    if os.name == "nt":
        try:
            try:
                board = pyfirmata.ArduinoNano(COM1)
            except:
                board = pyfirmata.ArduinoNano(COM2)
        except:
            print("Connection Failed, retrying in 5 seconds...")
            time.sleep(5)
            import_arduino()
            
    elif os.name == "posix":
        try:
            try:
                board = pyfirmata.ArduinoNano("/dev/ttyUSB0")
            except:
                board = pyfirmata.ArduinoNano("/dev/ttyUSB1")
            
        except:
            print("Connection Failed, retrying in 5 seconds...")
            time.sleep(5)
            import_arduino()
    
    return board
        
def map_x(value, min_v, max_v, min_wv, max_wv):
    if value <= max_v and value >= min_v:
        dvd = (max_wv - min_wv) + 1
        i = min_wv 
        dvd2 = max_v / dvd
        dvd3 = dvd2
        
        while i < dvd:
            if value <= dvd2:
                return i
                break
            elif value > dvd2: 
                dvd2 += dvd3 
            i-=-1
            
        if value <= dvd2:
            return max_wv

def list_to_str(input_settings):
    return (str("#".join(input_settings)) + "#")

def get_robo_loc2(potan, max_v):
    i1 = map_x(potan, 0, max_v, 0, 2)
    robo_loc = ""
    while range(3):
        if i1 == 2:
            robo_loc = "left"
            return robo_loc
            break
        elif i1 == 1:
            robo_loc = "middle"
            return robo_loc
            break
        elif i1 == 0:
            robo_loc = "right"
            return robo_loc
            break
        print("Potansiyometre cevap vermiyor")
        time.sleep(0.3)

def get_robo_loc(potan):    
    i1 = map_x(potan, 0, 1, 0, 2)
    robo_loc = ""
    while range(3):
        if i1 == 2:
            robo_loc = "left"
            return robo_loc
            break
        elif i1 == 1:
            robo_loc = "middle"
            return robo_loc
            break
        elif i1 == 0:
            robo_loc = "right"
            return robo_loc
            break
        print("Potansiyometre cevap vermiyor")
        time.sleep(0.3)

def addSetting(name, value, input_array):
    if input_array == []:
        input_array = ["tunapro"]
        
    # input_array.append(Setting(str(name), str(value)).return_list())
    input_array.append(str(Setting(name, value)))
    return input_array

def send_settings(input_str, tcp_port = 5800):
    connect_server(tcp_port)
    transmit_settings(input_str)

def connect_server(tcp_port = 5800):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:" + str(tcp_port))
    return socket
    
def start_server(tcp_port = 5800):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + str(tcp_port))
    return socket

def transmit_settings(input_settings, tcp_port):
    try:
        socket = start_server()
    except:    
        socket = connect_server(tcp_port)
        sending_str = list_to_str(input_settings)
        sending_str = str.encode(sending_str)
    
        socket.send(sending_str)
        ack = str(socket.recv())
        # print(str(ack))
        socket2 = connect_server(tcp_port+1)
        time.sleep(2)
        if ack == str(sending_str) and ack != None:
            socket2.send(b"OK")
            return "SENT"
        else:
            socket2.send(b"RETRY")
            return "RETRYING"
            time.sleep(4)
            transmit_settings(input_settings)
    else:
        return "SERVER NOT STARTED"
        
def test1(inp1):
    return map_x(inp1, 0, 1, 0, 30)
                

def whichIsChanged(digital_input1, digital_input2, analog_input1):
    # print("input: "   )
    but1 = None
    but1_p = None
    
    but2 = None
    but2_p = None
    
    pot1_p = test1(analog_input1.read())
    
    while True:
        if (but1_p != but1) and but1 > 0 and (not (but2 > 0)):
            but1 = but1_p
            return "button0"
            break
        
        elif (but2_p != but2) and but2 > 0 and (not (but1 > 0)):
            but2 = but2_p
            return "button1"
            break
        
        try:
            if (pot1_p != pot1):
                return pot1
        except:
            pass
        
        but1 = digital_input1.read()
        but2 = digital_input2.read()
        pot1 = test1(analog_input1.read())
        time.sleep(0.15)


# def whichIsChanged(digital_input1, digital_input2, analog_input1):
#     # print("input: "   )
#     but1 = None
#     but1_p = None
    
#     but2 = None
#     but2_p = None
    
#     pot1_p = test1(analog_input1.read())
    
#     while True:
#         if (but1_p != but1) and but1 > 0 and (not (but2 > 0)):
#             but1 = but1_p
#             return "button0"
#             break
        
#         elif (but2_p != but2) and but2 > 0 and (not (but1 > 0)):
#             but2 = but2_p
#             return "button1"
#             break
        
#         try:
#             if (pot1_p != pot1):
#                 return pot1
#         except:
#             pass
        
#         but1 = digital_input1.read()
#         but2 = digital_input2.read()
#         pot1 = test1(analog_input1.read())
#         time.sleep(0.15)
     
def whichIsChangedTest(digital_input1, digital_input2, analog_input1):
    print("input: ")
    but1 = None
    but1_p = None
    
    but2 = None
    but2_p = None
    
    pot1_p = test1(analog_input1.read())
    
    while True:
        if (but1_p != but1) and but1 > 0 and (not (but2 > 0)):
            but1 = but1_p
            return "button0"
            break
        
        elif (but2_p != but2) and but2 > 0 and (not (but1 > 0)):
            but2 = but2_p
            return "button1"
            break
        
        try:
            if (pot1_p != pot1):
                return pot1
        except:
            pass
        
        but1 = digital_input1.read()
        but2 = digital_input2.read()
        pot1 = test1(analog_input1.read())
        time.sleep(0.1)

# tcp_port = 5800
# settings = []

#region arduino
# board = pyfirmata.ArduinoNano("COM4")

#region component
# swt1 = board.get_pin("a:1:i")
# pot1 = board.get_pin("a:2:i")
# inp1 = board.get_pin("a:6:i")
# inp2 = board.get_pin("a:7:i")
# but1 = board.get_pin("d:2:i")
# led1 = board.get_pin("d:11:p")
#endregion
#region iterator
# iterator = Iterator(board)
# iterator.start()
# time.sleep(0.2)
#endregion
#endregion

# robo_loc = get_robo_loc(pot1.read())
# print(robo_loc)
# settings = addSetting("isTest", "True", settings)
# settings = addSetting("robot_location", robo_loc, settings)

# transmit_settings(settings, tcp_port)

# # connect_server(tcp_port)
# # transmit_settings(settings)

        
        
        
