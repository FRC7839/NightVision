from threading import Thread
from frc_lib7839 import *
import threading
import pyfirmata
import curses
import socket
import json
import time
import zmq
import os

global arduino_menu_value
global camera_menu_value
global main_menu_value
global ip_menu_value

arduino_menu_value = 2
camera_menu_value = 3
main_menu_value = 0
ip_menu_value = 1

####################### TODO ###########################
# WRITE CURRENT SETTING RETURN TO MAIN MENU            #
# Waiting periodu arduino ozele ekle                   #
# JSON okuma-yazma fonksyonlari                        #
# curses_functions ve eski isimlerin duzeltilmesi      #
# Kayranin socketlerinin tamamlnamasi                  #
# Mac menusunun hazirlanmasi                           #
########################################################

# deneme2
# write_settings_on_txt() fonksiyounu kullanrak dosyaydaki her seyi alip tekrar yazmasi gerekiyor

###################### CURSES CALISMA MANTIGI ##################################################
# ilk olarak get menu values functionlari bir array'a ekranda yazilacak her bir satiri atiyor. #
# her satir bir element oluyor ve surekli olarak get menu values fonksiyonunu elementler       #
# uzerinde islem yapip onlari degistiriyor                                                     #
# sonra print menu bunlari alip yerlerini hesapladiktan sonra ekrana yazdiriyor.               #
# bu bize get menu values kullanark ekrandaki goruntuyu aktif olarak degistirmemizi sagliyor.  #
################################################################################################


# DIKKAT
# Match mode otonom yuzunden diger tum menulerden farkli bir print 
# fonksiyonuna ve getvalues'a ihtiyac duyuyor
# match mode icin get menu values fonksiyonu

def match_mode(stdscr, settings, led1, out1, but1, but2, swt1, pot1, cur_stat):
    led_control = {}
    # Ana yer
    while True:        
        #Dosyadan okumayi dene
        try:
            read = DbFunctions.get_setting(file_lc) # led control dosyasindan ayari cekiyor    
        except:
            # if read.startswith("InputP") or read == None or read == "":
            #     ### ERROR HANDLE ###
            pass
        
        m_menu_elements = [] # Menu elementleri arrayi
        m_menu_elements.append(" ## MATCH MODE STARTED ## ") # Title
            
        # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
        if led_control["status"] is not None and led_control["status"] in [True, False, "True", "False"]: 
            m_menu_elements.append(" ## LED CONTROL : " + str(led_control["status"]) + " ## ")
      
      
        # Eger kapali yada acik alamazsa error veriyor.
        else:
            m_menu_elements.append(" ## LED CONTROL FAILED ## ")
            led_control["satatus"] = True 
        
            
        # Menunun geri kalani, durum reporu veriyor.
        m_menu_elements.append(" ## CAMERA_TOLERANCE : " + str(settings["Camera Tolerance"]) + " ## ")
        m_menu_elements.append(" ## ROBOT_LOCATION : " + str(settings["Robot Location"]) + " ## ")
        m_menu_elements.append(" ## WAITING_PERIOD : " + str(settings["Waiting Period"]) + " ## ")
        m_menu_elements.append(" ## AUTONOMOUS_MODE : " + str(settings["Autonomous Mode"]) + " ## ")
        
        
        if led_control["status"] in ["True", True]:
            ArduinoFunctions.led_write(led1, out1 , 1) # on
        
        elif not (led_control["status"] in ["False", False]):
            ArduinoFunctions.led_write(led1, out1, 0) # off
        
        else:
            ArduinoFunctions.led_write(led1, out1, 1) # on

        
        print_menu_for_match(stdscr, m_menu_elements, cur_stat)
        
        
        # Exit kodu
        if (
            ArduinoFunctions.map_xi(pot1.read(), 0, 1, 0, max_v) == max_v
            and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == 0
        ):
            break    


def get_first_menu_values(): 
    ipaddr_func = InputPFunctions.get_ipaddr()
    check_cam_func = InputPFunctions.check_cam()

    mainmenu = []
    mainmenucheck = []

    if ipaddr_func.startswith("127"):
        mainmenu.append("IP ADRESS: NOT CONNECTED")
        mainmenucheck.append(False) ## False

    elif not ipaddr_func.startswith("10.78.39"):
        mainmenu.append("NOT CONNECTED TO RADIO")
        mainmenucheck.append(False) ## False

    else:
        mainmenu.append("IP ADRESS: " + ipaddr_func)
        mainmenucheck.append(True)

    mainmenu.append("ARDUINO CONFIG")
    mainmenucheck.append(True)

    if check_cam_func == "CAMERA.PY CONNECTED" or check_cam_func == "TRUE BECAUSE WINDOWS":
        mainmenu.append(check_cam_func)
        mainmenucheck.append(True)
    else:
        mainmenu.append(str(check_cam_func))
        mainmenucheck.append(False) ## False

    mainmenu.append("LED TEST")
    mainmenucheck.append(True)

    mainmenu.append("EXIT")
    mainmenucheck.append("Normal")

    return [mainmenu, mainmenucheck]


def get_ip_menu_values(ssid_func=InputPFunctions.get_ssid(), ipaddr_func=InputPFunctions.get_ipaddr()):
    mainmenu = []
    mainmenu_status = []

    mainmenu.append("HOSTNAME: " + str(socket.gethostname()))
    mainmenu.append("SSID: " + str(ssid_func))
    mainmenu.append("IP ADRESS: " + ipaddr_func)
    mainmenu.append("OK")

    mainmenu_status.append("Normal")

    if str(socket.gethostname()) != "frcvision":
        mainmenu_status[0] = False

    if ipaddr_func.startswith("127"):
        mainmenu_status.append(False)
        mainmenu_status.append(False)
        mainmenu[2] = "IP ADRESS: NOT CONNECTED"

    elif ipaddr_func.startswith("10.78.39"):
        mainmenu_status.append(False)
        mainmenu_status.append(False)

    else:
        mainmenu_status.append("Normal")
        mainmenu_status.append("Normal")

    mainmenu_status.append("Normal")

    return [mainmenu, mainmenu_status]


def get_arduino_menu_values(settings):
    mainmenu = []
    mainmenu_status = []
    


    # ROBOT LOCATION
    if settings["Robot Location"] is None:
        mainmenu.append("INPUT FOR ROBOT LOCATION")
        mainmenu_status.append(False)

    else:
        mainmenu.append("ROBOT LOCATION: " + settings["Robot Location"])
        mainmenu_status.append("Normal")

    # CAMERA TOLERANCE
    if settings["Camera Tolerance"] is None:
        mainmenu.append("INPUT FOR CAMERA TOLERANCE")
        mainmenu_status.append(False)

    else:
        mainmenu.append("CAMERA TOLERANCE: " + settings["Camera Tolerance"])
        mainmenu_status.append("Normal")

    # WAITING PERIOD
    if settings["Waiting Period"] is None:
        mainmenu.append("INPUT FOR WAITING PERIOD")
        mainmenu_status.append(False)

    else:
        mainmenu.append("WAITING PERIOD: " + settings["Waiting Period"])
        mainmenu_status.append("Normal")

    # AUTONOMOUS MODE
    if settings["Autonomous Mode"] is None:
        mainmenu.append("INPUT FOR AUTONOMOUS MODE")
        mainmenu_status.append(False)
    else:
        mainmenu.append("AUTONOMOUS MODE: " + settings["Autonomous Mode"])
        mainmenu_status.append("Normal")

    # WRITE CURRENT SETTINGS AND OK BUTTONS
    mainmenu.append("WRITE CURRENT SETTINGS TO FILE")
    mainmenu_status.append("Normal")

    mainmenu.append("CANCEL")
    mainmenu_status.append("Normal")

    return [mainmenu, mainmenu_status]


def get_cam_menu_values(isCamOnline=InputPFunctions.check_cam()):
    mainmenu = []
    mainmenu_status = []

    # # ILK ELEMENT (NETWORK TABLES)
    # if msg:
    #     mainmenu.append("NETWORK TABLES CONNECTED")
    #     mainmenu_status.append(True)
    # if not msg:
    #     mainmenu.append("NETWORK TABLES NOT CONNECTED")
    #     mainmenu_status.append(False)
    # else:
    #     mianmenu.append("CAMERA.PY NOT STARTED")
    #     mainmenu_status.append(False)

    # IKINCI ELEMENT (IS CAM ONLINE)
    if isCamOnline:
        mainmenu.append("CAMERA CONNECTED")
        mainmenu_status.append(True)

    if not isCamOnline:
        mainmenu.append("CAMERA NOT CONNECTED")
        mainmenu_status.append(False)

    # OK BUTTON
    mainmenu.append("OK")
    mainmenu_status.append("Normal")

    return [mainmenu, mainmenu_status]


def print_error(stdscr, cur_stat):
    if cur_stat is not None:
        errmsg = cur_stat["current_error"]
        if errmsg is not None:
            h, w = stdscr.getmaxyx()
            x = w // 2 - (len(errmsg) + 1) // 2
            y = h - 1
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, errmsg)
            stdscr.attroff(curses.color_pair(2))
            screen.refresh()
    if cur_stat is None:
        h, w = stdscr.getmaxyx()
        x = (w // 2) - (1 // 2)
        y = h - 1
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(y, x, "")
        stdscr.attroff(curses.color_pair(2))
        screen.refresh()


def print_current_menu(stdscr, cur_stat):
    firsttime = True

    if type(cur_stat["current_menu_elements"][0]) is list:
        cur_stat["current_menu_elements"] = cur_stat["current_menu_elements"][0]

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(cur_stat["current_menu_elements"]):
        if cur_stat["current_menu_status"][idx]:
            colornumber = 3

        elif not cur_stat["current_menu_status"][idx]:
            colornumber = 2

        else:
            colornumber = 4

        x = w // 2 - (len(row) + 1) // 2
        y = h // 2 - (len(cur_stat["current_menu_elements"]) + 1 ) // 2 + idx

        if idx == cur_stat["current_row"]:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))

        else:
            stdscr.attron(curses.color_pair(colornumber))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(colornumber))
        
        if firsttime:
            firsty = y-1
            firsttime = False   
        elif not firsttime:
            pass

    
    for i in cur_stat["all_menu_elements"][main_menu_value][1]:
        if i:
            match_message = " ## MATCH MODE CAN BE STARTED ## "
            match_message_color = 4
        else:
            match_message = " ## MATCH MODE CANNOT BE STARTED ## "
            match_message_color = 2
            break

    firstx = w // 2 - (len(match_message) + 1) // 2

    stdscr.attron(curses.color_pair(match_message_color))
    stdscr.addstr(firsty - 1, firstx, match_message)
    stdscr.attroff(curses.color_pair(match_message_color))

    stdscr.refresh()


def print_menu_for_match(stdscr, m_menu_elements, cur_stat):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(m_menu_elements):
        x = w // 2 - (len(row) + 1) // 2
        y = h // 2 - (len(m_menu_elements) + 1 ) // 2 + idx

        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(y, x, row)
        stdscr.attroff(curses.color_pair(4))
  
    stdscr.refresh()


def cursor_handler(key, cur_stat):
    # Imlec Asagi
    current_row = cur_stat["current_row"]

    if (key == "button1") and (
        current_row < (len(cur_stat["current_menu_elements"]) - 1)
    ):

        current_row += 1

    # Imlec Dongu
    elif (
        current_row == (len(cur_stat["current_menu_elements"]) - 1) and key == "button1"
    ):

        current_row = 0

    return current_row


def change_menu(key, cur_stat, led1, out1):
    if key == "button0" and cur_stat["current_menu"] == main_menu_value:
        
        # IP MENU
        if cur_stat["current_row"] == 0:
            new_menu = ip_menu_value
            new_row = 0

        
        # ARDUINO CONFIG MENU
        elif cur_stat["current_row"] == 1:
            new_menu = arduino_menu_value
            new_row = 0
         
        # CAMERA MENU
        elif cur_stat["current_row"] == 2:
            new_menu = camera_menu_value
            new_row = 0

        # LED TEST
        elif cur_stat["current_row"] == 3:
            ArduinoFunctions.led_write(led1, out1, 0)
            time.sleep(1)
            ArduinoFunctions.led_write(led1, out1, 1)
            new_menu = cur_stat["current_menu"]
            new_row = cur_stat["current_row"]

        #EXIT
        elif cur_stat["current_row"] == len(cur_stat["all_menu_elements"][main_menu_value][0]) - 1:
            new_menu = cur_stat["current_menu"]
            new_row = cur_stat["current_row"]
            exit()
        
    else:
        new_row = cur_stat["current_row"]
        new_menu = cur_stat["current_menu"]
        
    return new_row, new_menu


def return_to_menu(key, cur_stat):
    # Ana Menuye Cikma
    if (
        (key == "button0")
        and cur_stat["current_menu"] != 0
        and cur_stat["current_row"] == (len(cur_stat["current_menu_elements"]) - 1)
    ):
        cur_stat["current_row"] = 0
        cur_stat["current_menu"] = 0

    return cur_stat["current_row"], cur_stat["current_menu"]


def background_setup(stdscr, cur_stat):
    if cur_stat["current_menu"] == 0:
        for i in cur_stat["current_menu_status"]:
            if i:
                stdscr.bkgd(" ", curses.color_pair(3))

            elif not i:
                stdscr.bkgd(" ", curses.color_pair(2))
                break

    elif cur_stat["current_menu"] != 0:
        stdscr.bkgd(" ", curses.color_pair(4))


def refresh_screen(stdscr, cur_stat, key, ntmsg, settings):
    new_all_menu_elements = cur_stat["all_menu_elements"]

    errmsg = cur_stat["current_error"]

    new_all_menu_elements[main_menu_value] = get_first_menu_values()
    new_all_menu_elements[ip_menu_value] = get_ip_menu_values(InputPFunctions.get_ssid(), InputPFunctions.get_ipaddr())
    new_all_menu_elements[arduino_menu_value] = get_arduino_menu_values(settings)
    new_all_menu_elements[camera_menu_value] = get_cam_menu_values()

    # cur_stat["all_menu_elements"] = new_all_menu_elements
    # cur_stat["current_menu_elements"] = new_all_menu_elements[c"ur_stat["current_menu"]]

    # Background seysi
    background_setup(stdscr, cur_stat)

    # Background ayarlandiktan sonra menu yazdirildi
    print_current_menu(stdscr, cur_stat)

    return new_all_menu_elements



def not_main(stdscr):

    
    msg = None
    key = None
    # region arduino import

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


    # endregion

    
    #region Settings okuma,,    
    settings = DbFunctions.get_setting(file=file_s) 
    
    if settings == "ERROR":
        cur_stat["current_error"] = all_errors["READ_ERROR"]

    for setting_name in setting_names:
        try:
            settings[setting_name]
        except KeyError:
            ### ERROR ###
            print("InputP: Setting not found on json file...")
    
    #endregion
    
    ArduinoFunctions.led_write(led1, out1, 1)


    # region while dongusune kadar olan gereksiz seyler
    # Tum menu elemanlari all_menu_elemants adinda bir fonksiyon icinde duruyor
    # Sebebini sormak sizin gercekten zeki oldugunuzu gosterir
    # Neden oldugunu bilmiyorum, sadece boyle daha karmasik ve daha havali duruyor
    all_menu_elements = []
    all_menu_elements.append(get_first_menu_values())
    all_menu_elements.append(get_ip_menu_values())
    all_menu_elements.append(get_arduino_menu_values(settings))
    all_menu_elements.append(get_cam_menu_values(None))

    # Imlec konumu
    current_row = 0
    # Aktif olan menu
    current_menu = 0
    # Aktif olan menudeki elemanlar
    current_menu_elements = all_menu_elements[0][0]
    # Aktif olan menudeki elemanlarin renk degerleri
    current_menu_status = all_menu_elements[0][1]
    
    cur_stat = {
        "current_row": current_row,
        "current_menu": current_menu,
        "current_menu_elements": current_menu_elements,
        "current_menu_status": current_menu_status,
        "all_menu_elements": all_menu_elements,
        "current_error" : None
    }
    
    # Dosyaya kaydedilmis olmasi gereken degiskenlerin atanmasi
    # camera_tolerance = DbFunctions.read_setting_on_txt("camera_tolerance", file)
    # robot_location = DbFunctions.read_setting_on_txt("robot_location", file)
    # waiting_period = DbFunctions.read_setting_on_txt("waiting_period", file)
    

    # RENKLER
    # 2 = RED
    # 3 = GREEN
    # 4 = NORMAL

    # region curses background set

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # endregion

    # Kodun calisip calismadipini anlamak icin kullandigimiz port 5802
    # Ve ledin kapanip acma bilgisinin yazildigi port da 5803
    
    #endregion

    while True:
        
        ##########
        # Ekran yenilenmesi
        cur_stat["all_menu_elements"] = refresh_screen(stdscr, cur_stat, key, msg, settings=settings)

        # Error mesaji silinmesi
        if cur_stat["current_error"] is not None:
            errortimer = threading.Timer(5, print_error, args=[stdscr, None])
            errortimer.start()
        else:
            print_error(stdscr, cur_stat)

        # Basilan key deger okundu
        key, msg = ArduinoFunctions.key_get(but1, but2, pot1, wait_time_to_get_key)
        
        # Imlec hareketleri degiskenlere yazildi
        cur_stat["current_row"] = cursor_handler(key, cur_stat)

        ##########

        for i in cur_stat["all_menu_elements"][main_menu_value][1]:
            if i:
                kayra_tam_bir_gerizekali = True

            elif not i:
                kayra_tam_bir_gerizekali = False
                break

        # Mac Modu
        if (
            kayra_tam_bir_gerizekali == True
            and ArduinoFunctions.map_xi(pot1.read(), 0, 1, 0, max_v) == 0
            and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == max_v
            and cur_stat["current_menu"] == main_menu_value
        ):               
            # print("sex")
            match_mode(stdscr, settings, led1, out1, but1, but2, swt1, pot1, cur_stat)
            
        # region arduino menu ozel
        if cur_stat["current_menu"] == 2:
            if (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 0
            ):
                settings["Robot Location"] = ArduinoFunctions.get_robo_loc_from_inp(key, max_v)

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 1
            ):
                settings["Camera Tolerance"] = str(key)

            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 2
            ):
                settings["Waiting Period"] = str(key//2)


            elif (
                key not in ["button1", "button0", "switch on", "switch off"]
                and cur_stat["current_row"] == 3
            ):
                settings["Autonomous Mode"] = str(ArduinoFunctions.map_x(key, 0, max_v, 0, 5))

            # Send tusu
            if (
                key == "button0"
                and cur_stat["current_row"] == 4
            ):
                
                DbFunctions.save_settings(settings, file_s)
                
                # if waiting_period is not None:
                #     DbFunctions.write_setting_to_txt(waiting_period, file)
                
            all_menu_elements[2] = get_arduino_menu_values(settings)

            cur_stat["current_menu_elements"] = all_menu_elements[2][0]
            cur_stat["current_menu_status"] = all_menu_elements[2][1]

        # Eger Arduino menusunden cikilirsa Server tekrar kontrol edilecek

        # endregion


        # Menu degistirme olaylari
        cur_stat["current_row"], cur_stat["current_menu"] = change_menu(key, cur_stat, led1, out1)
        cur_stat["current_row"], cur_stat["current_menu"] = return_to_menu(key, cur_stat)

        if cur_stat["current_menu"] == 0:
            cur_stat["current_menu_elements"] = all_menu_elements[0][0]
            cur_stat["current_menu_status"] = all_menu_elements[0][1]

        elif cur_stat["current_menu"] == 1:
            cur_stat["current_menu_elements"] = all_menu_elements[1][0]
            cur_stat["current_menu_status"] = all_menu_elements[1][1]

        elif cur_stat["current_menu"] == 2:
            cur_stat["current_menu_elements"] = all_menu_elements[2][0]
            cur_stat["current_menu_status"] = all_menu_elements[2][1]

        elif cur_stat["current_menu"] == 3:
            cur_stat["current_menu_elements"] = all_menu_elements[3][0]
            cur_stat["current_menu_status"] = all_menu_elements[3][1]


curses.wrapper(not_main)

# region def main
# def main():
#     try:
#         curses.wrapper(not_main)
#     except:
#         time.sleep(1)
#         print("An error occured restarting in 5 seconds...")
#         time.sleep(5)
#         main()
#
# if __name__ == "__main__":
#     main()
# endregion
