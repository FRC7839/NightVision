from frc_lib7839 import * 
import numpy as np
import timeit
import time
import json
import math
import cv2
import zmq
import os

# Alttaki socket.send() fonksiyonunun içine değer ver


# def go_left():
#     pass


# def go_right():
#     pass


cap = cv2.VideoCapture(0)


cap.set(3, 480)
cap.set(4, 640)
cap.set(cv2.CAP_PROP_EXPOSURE, -9)


def main():
    print("Started...")

    cam_tol = int(settings["Camera Tolerance"])
    settings = DbFunctions.get_setting(file_s)
    ip_addr = ServerFunctions.get_ipaddr()
    robo_loc = settings["Robot Location"]
    ip_addr = "127.0.0.1"
    isNtStarted = True
    y_error = None
    
    if True:
        isConntedtoRadio = True
        try:
            # NetworkTables.initialize()
            print("Network Tables initialize")
        except:
            ### ERROR 001-test_version###
            print("NT NOT STARTED")
        else:
            isNtStarted = True
    else:
        isConntedtoRadio = False

    if isNtStarted:
        # outputStream = cs.putVideo("LQimg", 120, 90)
        print("outputStream = cs.putVideo('LQimg', 120, 90)")

    # outputStream = cs.putVideo("LQimg", 120, 90)

    text_font = cv2.FONT_HERSHEY_SIMPLEX
    _name = ""

    while True:
        success = False
        ok_contours = []
        _, frame = cap.read()
        
        contours = CameraFunctions.detect_targets(frame)
        
        try:
            for cnt in contours:
                _ok, _name = CameraFunctions.cnt_test(cnt)
                if _ok:
                    ok_contours.append(cnt)
                success = True
        except TypeError:
            pass

        final_result = frame
        if len(ok_contours) >= 1:
            final_result = CameraFunctions.draw_rectangle(frame, ok_contours)
            cv2.putText(
                final_result, _name, (30, 50), text_font, 1, (0, 0, 255), 2, cv2.LINE_AA
            )
            success, y_error, distance = CameraFunctions.calculate_errors(ok_contours)
            # for c in ok_contours:
            #     cv2.drawContours(final_result, c, -1, (255, 0, 0), 2)
        cv2.imshow("FRC Vision", final_result)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        
        ###############################################################################################
        # 
        # 
        # 
        #   
        
        # Led kontrol'u 5803ncu port uzerinden yolluyor, server'a baglanamazsa geciyor
        
        # led_control = True #  <----------------------- GECICI, KALDIRMAMIZ LAZIM <-------------

        # start_t = timeit.default_timer()
        
        # isServer5802Started = ServerFunctions.check_server(is_input_started)
        # isServer5803Started = ServerFunctions.check_server(led_control_port)
        
        # if isServer5802Started and isServer5803Started:
        #     try:
        #         socket5803 = ServerFunctions.connect_to_server(led_control_port)
        #         ServerFunctions.send_to_server(socket5803, led_control)
        #         socket5803.close()
        #     except:
        #         pass

        # if isServer5802Started:
        #     socket5802 = ServerFunctions.connect_to_server(is_input_started)
        #     ServerFunctions.send_to_server(socket5802, isNtStarted)
        #     socket5802.close()
                
        # elapsed = timeit.default_timer()        
        # elapsed = elapsed - start_t
        # print(elapsed)
        
        ###############################################################################################
        
        led_control = DbFunctions.save_settings(led_control, file=file_lc)

        if success == True and y_error is None:
            success = False

        try:
            # print("Success: " + str(success), "Error: " + str(y_error), "Distance: " + str(distance), sep="  --  ")
            if (success == True) and (
                y_error < (-1 * cam_tol)
            ):  # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın sağında kalıyorsa ve servo en sağda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Hedef sağda",
                    sep="  --  ",
                )

                # go_right()

            elif (success == True) and (
                y_error > cam_tol
            ):  # Eğer herhangi bir obje aktif olarak görülüyorsa, objenin orta noktası ekranın solunda kalıyorsa ve servo en solda değilse
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Hedef solda",
                    sep="  --  ",
                )
                # go_left()

            elif (
                (success == True) and (y_error < cam_tol) and (y_error > (-1 * cam_tol))
            ):
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Hedef ortada",
                    sep="  --  ",
                )

            else:
                print(
                    "Success: " + str(success),
                    "Error: " + str(y_error),
                    "Distance: " + str(distance),
                    "Robot location: " + robo_loc,
                    "Camera Tolerance: " + str(cam_tol),
                    "Hedef bulunamadı",
                    sep="  --  ",
                )

        except UnboundLocalError:
            pass

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
