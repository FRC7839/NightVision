from frc_lib7839 import *
import pyfirmata
import socket 
import time
import json

# BU KOD SAKAT TUNAPRONUN DENEMELERİ İÇİNDİR LÜTFEN İNCELEMEYİN

board = ArduinoFunctions.import_arduino()
# board = pyfirmata.ArduinoNano("COM4")

swt1 = board.get_pin("a:1:i")
pot1 = board.get_pin("a:2:i")
inp1 = board.get_pin("a:6:i")
out1 = board.get_pin("d:10:p")
but1 = board.get_pin("d:2:i")
but2 = board.get_pin("d:7:i")
led1 = board.get_pin("d:11:p")

iterator = pyfirmata.util.Iterator(board)
iterator.start()
time.sleep(0.2)

def main():
    
    print(ArduinoFunctions.map_xi(pot1.read(), 0, 1, 0, 30))


    # endregion
    # key, msg = ArduinoFunctions.key_get_with_recv(arduino_pins)
    # print(key)
        
    
if __name__ == "__main__":
    while True:
        main()
        time.sleep(0.5)