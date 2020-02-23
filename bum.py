from frc_lib7839 import *

def main():
    com_ports = ArduinoFunctions.check_ports()
    
    if com_ports is not None:     
        board = ArduinoFunctions.import_arduino(com_ports)
        if type(board) == str and board.startswith("InputP"):
            time.sleep(wait_time_for_get_key)
            main()
    else:
        main()
        
    enc_but = board.get_pin("d:2:i")
    enc_out_b = board.get_pin("d:3:i")
    enc_out_a = board.get_pin("d:4:i")
    led1 = board.get_pin("d:5:i")
    swt1 = board.get_pin("d:6:i") 
    # led_set = board.get_pin("d:7:o")
    led_change = board.get_pin("d:8:o")
    
    iterator = pyfirmata.util.Iterator(board)
    iterator.start()
    time.sleep(0.2)
    
    print("Waiting for key")
    
    while True:
        key, rv = ArduinoFunctions.encoder_key_get(enc_out_a, enc_out_b, enc_but, wait_time_for_get_key)
        print(key)
    
if __name__ == "__main__":
    main()