from pyfirmata.util import Iterator 
import curses_functions
import pyfirmata
import time
import zmq
import os

def main():
    tcp_port = 5800 
    settings = []

    settings = curses_functions.addSetting("isTest", "True", settings)
    settings = curses_functions.addSetting("robot_location", "middle", settings)    
    
    print(settings)
    
    test = curses_functions.transmit_settings(settings, tcp_port)
    print(test)

if __name__ == "__main__":
    main()