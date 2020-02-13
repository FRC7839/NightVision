from  pyfirmata.util import Iterator
import pyfirmata
import time
import curses_functions

def main():
    board = pyfirmata.ArduinoNano("COM3")
    but1 = board.get_pin("d:2:i")
    but2 = board.get_pin("d:7:i")
    pot1 = board.get_pin("a:2:i")
    
    iterator = Iterator(board)
    iterator.start()
    time.sleep(0.2)
    print(curses_functions.whichIsChangedTest(but1, but2, pot1))
    
def test1(inp1):
    return curses_functions.get_robo_loc(inp1)

    
if __name__ == "__main__":
    main()        