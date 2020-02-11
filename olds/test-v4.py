import numpy as np
import pyfirmata
import math
import time
import cv2

global board

try:
    board = pyfirmata.Arduino("COM3")
except:
    board = pyfirmata.Arduino("COM4")

try:
    cap = cv2.VideoCapture(1)
except:
    print("Tuna, kamera")
    cap = cv2.VideoCapture(0)

cap.set(3, 480)
cap.set(4, 640)
cap.set(cv2.CAP_PROP_EXPOSURE, -9)

cam_tolerance = 15



class Servo:
    def __init__(self, pin, speed=1, angle=0, mina=0, maxa=180):
        self.pin = board.get_pin(pin)
        self.speed = speed
        self.angle = angle
        self.mina = mina
        self.maxa = maxa
        
    def add_angle(self, tunawashere):  # servonun belirli bir tarafa, belirli bir açıda döndürlmesi için
        self.angle += tunawashere  # servonun açısına verilen açı ekleniyor
        self.pin.write(self.angle)
        # board.get_pin(self.pin).write(self.angle)
        
    def set_angle(self, setting_angle):  # servonun belirli bir açıya döndürülmesi için
        self.angle = setting_angle
        self.pin.write(self.angle)
        # board.get_pin(self.pin).write(self.angle)


def main():
    print("Started...")
    gol = True 
    servo1 = Servo("d:9:s")
    servo1.set_angle(0)
    success = False

   
    text_font = cv2.FONT_HERSHEY_SIMPLEX
    _name = ""
    functions = Functions()
    while True:
        success = False 
        ok_contours = []
        _, frame = cap.read()   

        contours = functions.detect_targets(frame)
        
        try:
            for cnt in contours:
                _ok, _name = functions.cnt_test(cnt)
                if _ok:
                    ok_contours.append(cnt)
                success = True
        except TypeError:
            pass
            
        final_result = frame
        if len(ok_contours) >= 1:
            final_result = functions.draw_rectangle(frame, ok_contours)
            cv2.putText(final_result, _name, (30, 50), text_font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            success, y_error, distance = functions.calculate_errors(ok_contours)
            # for c in ok_contours:
            #     cv2.drawContours(final_result, c, -1, (255, 0, 0), 2)
        cv2.imshow('FRC Vision', final_result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        try:
            if (success == True and y_error == None):
                print("Bunu okuyorsan siyabend gerizekalıdır")
        except UnboundLocalError:
            if (success == True):
                success = False
            
        #####################################################################################################
        #region servo1

        if (success == False and servo1.angle <= (servo1.maxa - servo1.speed) and gol == True):  # Eğer herhangi bir obje aktif olarak görülmüyorsa, servo en sola gelmediyse ve tunanın saçma değişkeni true ise      
            gol = True           # Tuna'nın şaçma değişkeni nedense True yapıldı
            servo1.add_angle(servo1.speed)   # Servo bir derece sola döndürüldü

        elif success == False and ((servo1.angle == servo1.maxa) or (gol == False)):  # Eğer herhangi bir obje aktif olarak görülmüyorsa ve servo en sola geldiyse "ya da" herhangi bir obje aktif olarak görülmüyorsa ve daha önce sağa doğru dönmeye başlanmışsa       
            gol = False  # Sağa dönme işlemine başlatıldığını belirtmek için
            servo1.add_angle(-1 * servo1.speed)  # buraları cidden incelemiyorsun değil mi
        
            if servo1.angle == servo1.mina:  # Eğer en sağa gelindiyse
                gol = True  # Servonun sola dönme işlemini yapabilmesi için

        #endregion
        #####################################################################################################

        try:
            # print("Success: " + str(success), "Error: " + str(y_error), "Distance: " + str(distance), sep="  --  ")
            if ((success == True) and (y_error < (-1 * cam_tolerance))): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Servo Angle" + str(servo1.angle),
                    "Hedef sağda",
                    sep="  --  ",
                )
                
                if (servo1.angle > (servo1.mina + servo1.speed)):
                    servo1.add_angle(-1 * servo1.speed) # Servoyu hafifçe sağa döndür,
                    time.sleep(0.05)
                    gol = False
                    
                 
            elif ((success == True) and (y_error > cam_tolerance)): # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın solunda kalıyorsa ve servo en solda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Servo Angle" + str(servo1.angle),
                    "Hedef solda",
                    sep="  --  ",
                )
                
                if (servo1.angle < (servo1.maxa - servo1.speed)):
                    servo1.add_angle(servo1.speed) # Servoyu hafifçe sola döndür
                    time.sleep(0.05)
                    gol = True
 
            elif ((success == True) and (y_error < cam_tolerance) and (y_error > (-1 * cam_tolerance))):
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Servo Angle" + str(servo1.angle),
                    "Hedef ortada",
                    sep="  --  ",
                )        

            else:
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Servo Angle" + str(servo1.angle),
                    "Hedef bulunamadı",
                    sep="  --  ",
                )      
            
        except UnboundLocalError:
            pass

    cap.release()
    cv2.destroyAllWindows()


class Functions:
    @staticmethod
    def detect_targets(capture):
        kernel = np.ones((3, 3), np.uint8)
        kernel2 = np.ones((13, 13), np.uint8)

        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        lower_green = np.array([45, 110, 105])
        upper_green = np.array([102, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        cv2.imshow("sl", mask)

        filter2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        filter3 = cv2.morphologyEx(filter2, cv2.MORPH_CLOSE, kernel2)

        _, contours, _ = cv2.findContours(filter3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    @staticmethod
    def draw_rectangle(_frame, contours):
        if not (len(contours)):
            return _frame

        contour = contours[0]

        rect = cv2.minAreaRect(contour)
        box_points = cv2.boxPoints(rect)
        box1 = np.int0(box_points)
        cv2.drawContours(_frame, [box1], 0, (0, 0, 255), 2)
        return _frame

    @staticmethod
    def cnt_test(cnt):
        rect = cv2.minAreaRect(cnt)

        # rect_width = min(rect[1][0], rect[1][1])
        # rect_height = max(rect[1][0], rect[1][1])
        # rect_angle = rect[2]

        box = cv2.boxPoints(rect)

        corner1x, corner1y = box[0]
        corner2x, corner2y = box[1]
        corner3x, corner3y = box[2]
        corner4x, corner4y = box[3]

        x_list = list((corner1x, corner2x, corner3x, corner4x))
        x_list.sort()
        y_list = list((corner1y, corner2y, corner3y, corner4y))
        y_list.sort()

        rect_width = abs(x_list[0] - x_list[2])
        rect_height = abs(y_list[0] - y_list[2])

        horizontal_friction = False
        vertical_friction = False

        for x_coord in x_list:
            horizontal_friction = bool(not (5 < x_coord < 635))
            if horizontal_friction:
                break

        for y_coord in y_list:
            vertical_friction = bool(not (5 < y_coord < 475))
            if vertical_friction:
                break

        if rect_width and rect_height and \
                not horizontal_friction and not vertical_friction and cv2.contourArea(cnt) > 250:
            rect_ratio = rect_width / rect_height
            if 1 > rect_ratio > 0:
                return True, "Loading Area"
            elif 1 <= rect_ratio <= 10:
                return True, "Target Area"
        else:
            return False, ""

    @staticmethod
    def calculate_errors(contours):
        try:
            cnt = contours[0]
        except IndexError:
            return False, 0
        rect = cv2.minAreaRect(cnt)
        box_p = cv2.boxPoints(rect)
        box = np.int0(box_p)

        moment1 = cv2.moments(box)
        center1x = int(moment1['m10'] / moment1['m00'])
        center1y = int(moment1["m01"] / moment1["m00"])
        camera_height = 40
        target_height = 300
        camera_angle = 75
        target_angle = (180 - center1y) / 180 * 43.30
        distance = (target_height - camera_height) / math.tan(camera_angle + target_angle)
        y_error = 320 - center1x
        return True, y_error, distance


if __name__ == "__main__":
    main()
