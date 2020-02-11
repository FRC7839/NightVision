from frc_lib7839 import *
import pyfirmata
import socket 
import time
import json

# region
# BU KOD SAKAT TUNAPRONUN DENEMELERİ İÇİNDİR LÜTFEN İNCELEMEYİN

# board = ArduinoFunctions.import_arduino()
# # board = pyfirmata.ArduinoNano("COM4")

# swt1 = board.get_pin("a:1:i")
# pot1 = board.get_pin("a:2:i")
# inp1 = board.get_pin("a:6:i")
# out1 = board.get_pin("d:10:p")
# but1 = board.get_pin("d:2:i")
# but2 = board.get_pin("d:7:i")
# led1 = board.get_pin("d:11:p")

# iterator = pyfirmata.util.Iterator(board)
# iterator.start()
# time.sleep(0.2)

# print(key)

# def key_get(
#     digital_input1,
#     digital_input2,
#     analog_input1,
#     wait_time=0.11,
#     func=None,
#     *args
#     ):
    
#     key = None
#     msg = None

#     but1 = None
#     but1_p = None

#     but2 = None
#     but2_p = None
    
#     pot1_p = ArduinoFunctions.map_xi(analog_input1.read(), 0, 1, 0, 30)
#     pot1 = pot1_p

#     while True:

#         if (but1 != but1_p) and but2 > 0 and (not (but2 > 0)):
#             but1 = but1_p
#             key = "button0"

#         elif (but2 != but2_p) and but2 > 0 and (not (but1 > 0)):
#             but2 = but2_p
#             key = "button1"
        
#         elif (pot1_p != pot1):
#             key = pot1
        
#         if func is not None:
#             ##
#             start_t = timeit.default_timer()
#             ##
            
#             rv = func(*args)
            
#             ##
#             elapsed = timeit.default_timer() - start_t
#             ##
            
#             if elapsed > wait_time:
#                 pass
            
#             else:
#                 time.sleep(wait_time - elapsed)
            
#         else:
#             time.sleep(wait_time)
            
#         if key is not None:
#             return key, rv

#         but1 = digital_input1.read()
#         but2 = digital_input2.read()
#         pot1 = ArduinoFunctions.map_xi(analog_input1.read(), 0, 1, 0, 30)
# endregion


def main():
    while True:
        time.sleep(1)
        
        
        
        
if __name__ == "__main__":
    # while True:
    main()
        # time.sleep(0.5)