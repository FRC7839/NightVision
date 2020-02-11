import pyfirmata
import time

global board
board = pyfirmata.Arduino("COM3")




class Servo:
    def __init__(self, pin, angle=0):
        self.pin = board.get_pin(pin)
        # self.pin = pin
        self.angle = angle
    
    def add_angle(self, tunawashere):  # servonun belirli bir tarafa, belirli bir açıda döndürlmesi için
        self.angle += tunawashere  # servonun açısına verilen açı ekleniyor
        self.pin.write(self.angle)
        # board.get_pin(self.pin).write(self.angle)
        
    def set_angle(self, setting_angle):  # servonun belirli bir açıya döndürülmesi için
        self.angle = setting_angle
        self.pin.write(self.angle)
        # board.get_pin(self.pin).write(self.angle)



def main():
   
    gor = True 
    servo1 = Servo("d:9:s")
    servo1.set_angle(0)
    success = False
    
    while True:  
        if (success == False and servo1.angle < 180 and gor == True):  # Eğer herhangi bir obje aktif olarak görülmüyorsa, servo en sola gelmediyse ve tunanın saçma değişkeni true ise      
            gor = True           # Tuna'nın şaçma değişkeni nedense True yapıldı
            servo1.add_angle(1)   # Servo bir derece sola döndürüldü

        elif success == False and (servo1.angle == 180 or gor == False):  # Eğer herhangi bir obje aktif olarak görülmüyorsa ve servo en sola geldiyse "ya da" herhangi bir obje aktif olarak görülmüyorsa ve daha önce sağa doğru dönmeye başlanmışsa       
            gor = False  # Sağa dönme işlemine başlatıldığını belirtmek için
            servo1.add_angle(-1)  # buraları cidden incelemiyorsun değil mi
        
            if servo1.angle == 0:  # Eğer en sağa gelindiyse
                gor = True  # Servonun sola dönme işlemini yapabilmesi için

        # else:  # Öylesine
        #     print("Servo algoritmasında bilinmeyen hata...")

        time.sleep(0.001)
        
        
        
        
        
    


if __name__ == "__main__":
    main()