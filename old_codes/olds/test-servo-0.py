import pyfirmata

board = pyfirmata.Arduino("COM3")
servo1 = board.get_pin("d:9:s")
servo_angle = 0

while True:
    
    while servo1 <= 180:
        servo1.write(servo_angle)
         






