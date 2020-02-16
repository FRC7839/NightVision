#########################################################################################################
###
### WRITTEN BY:
### 
### ColonelKai - Kayra Acar
### TUNAPRO1234 - Tuna Gul
### BLACKSHADOW - Siyabend Urun
### 
### FRC 2020 - NightVision - Target Detection Algorithm 
### 
### NightFury#7839 (Adımız şu an farklı olabilir tartışmalar hala devam ediyor)
### 
#########################################################################################################


#                                                                  -->> . <<--NOKTAYI SİLME KOD BOZULUYOR
#                                                                      /\   HERKES LORD NOKTA KARSISINDA EGILSIN
#                                                                      |    TANRIMIZ NOKTA 
#                                                                      |
#                                               if you look to your above, you can see programmers going nuts

"""#####################################################################################################################"TODO"
                                                                                                                        
                                                                            14/2 TAKIM NUMARASINA GÖRE AYAR YAPIMI (OK)
                                                                            14/2 SET UP LED CONTROLLING SYSTEM (For Interface)
                                                                            14/2 Led kontrol içine robot ayarları yazılma hatasını düzelt
                                                                            14/2 FRC7839-NightVision yazısını yukarı sağ veya sol köşeye yaz (COLONELKAI)
                                                                            14/2 WRITE CURRENT SETTING RETURN TO MAIN MENU (COLONELKAI)
                                                                            14/2 INFO menüsü (Yazanlar - Tarih - Takım - vs) (COLONELKAI)
                                                                            14/2 check_arduino() oluştur ve key get içine koy
# Panic mode içinde tekrar arduinoyu takmayı dene 

# Save ve get_settings için handle_error()

# Led dosyasına is mm started ayarını ekle (Kamera algoritmasının okuyup okumaması gerektiğini söylemek için)

# ARDUINO IMPORT SUCCESS Mesajı ekranda kalmıyor (refresh yüzünden) (COLONELKAI)
                                                                                                                        
# Pyfirmata knob 28 kodu editlenmesi

# Yazılar üzerindeki türkçe karakterleri kaldır (ç, ı, İ, ö, ş, ü)
"TODO"########################################################################################################################"""

###############################################################################################################################
## 
##
## Eğer https://github.com/FRC7839/NightVision'deki ReadMe.md dosyasını okuduysanız muhtemelen burayı okumanıza
## gerek kalmayacaktır. Kodu istediğiniz gibi kullanın sadece isim vermemeniz beni cidden üzerdi.
##
##  
##  InputPlus.py Nedir Ne İşe Yarar Bu Yazılımı Kullanmak İçin Sebepler Nelerdir:
##
##
##      Öncelikle eğer bu yazılımı FRC2020 için almayı düşünüyorsanız cidden gecikme için çooook özür diliyorum.
##  Ama tatilde algoritmayı geliştirmesi için biraz Siyabendi bekledim ve robot olmadığı için servoyla farklı bir
##  prototip tasarlamam filan gerekti her neyse.
##
##
##      InputPlus.py sadece arayüz olması sebebiyle her sene tekrar kullanılabilecek bir koddur. Sadece algoritmayı
##  yenilemek sizin için yeterli olacaktır. Kodu biraz incelersiniz hata vermemesi için elimizden gelen her şeyi 
##  yaptığımızı görebilirsiniz. Eğer algılama ya da okuma gibi hatalar alırsanız InputPlus, kendini PANIC MODE'a alır
##  ve ledin kapanmasını önleyip ayarları dosyaya yazmaya çalışır. Algoritmayla kod sadece bir JSON dosyası üzerinden 
##  iletişim kurudukları için herhangi bir yazılımın çökmesi diğerinin de çökmesine sebep olmaz. 
##
##
##      Programı yönetbilmek için github sayfamızda açıklanan şekilde bağlanmış bir adet arduino, bir adet potansiyometre,
##  iki  adet regular push button ve ledlerin ve arduinonun girişi için dişi headerlar kullanılabilir. Ayrıca bir adet 
##  Raspberry pi, rpi için ekran kullanmalısınız (kap kullanmanızı öneririm).
##
##
##      Github sayfasını FRC 2020 Bosphorus Regional'dan sonra herkesin düzenlemesi için public hale getirmeye çalışacağım.
##
##
#########################################################################################################
##                                                                                                     ##                 
##  --skip-camera-check     : camera kontorlünü atlıyor (Zaten windowsta kamera kontrolü yok)          ##                                               
##  --skip-network-check    : ip adres kontrolünü atlıyor (NOT CONNECTED TO RADIO Hatası kapanıyor)     ##                                                   
##  --pc-mode               : skip camera ve skip networkün birleşimi                                  ##                       
##  --test-mode             : verilen hatalar programı durdurur (FRC esnasında önermiyorum)            ##                                           
##  --pc-test-mode          : pc ve test modunun birleşimi                                             ##           
##                                                                                                     ##         
#########################################################################################################



###################### CURSES CALISMA MANTIGI ##################################################
# ilk olarak get menu values functionlari bir array'a ekranda yazilacak her bir satiri atiyor. #
# her satir bir element oluyor ve surekli olarak get menu values fonksiyonunu elementler       #
# uzerinde islem yapip onlari degistiriyor                                                     #
# sonra print menu bunlari alip yerlerini hesapladiktan sonra ekrana yazdiriyor.               #
# bu bize get menu values kullanark ekrandaki goruntuyu aktif olarak degistirmemizi sagliyor.  #
################################################################################################



from threading import Thread
from FRC_LIB7839 import *
import threading
import pyfirmata
# import socket
import curses
# import zmq
import json
import time
import os

# region global

global pc_test_mode
global skip_cam_arg
global skip_nt_arg
global test_mode
global pc_mode
global team_ip2


team_number = InputPFunctions.find_arg("--team-number", num=True)

if team_number is None:
    team_ip2 = "78.39"
    
else:
    team_ip2 = str(InputPFunctions.find_arg("--team-number"))    
    
    if len(team_ip2) == 3:
        team_ip2 = "0" + team_ip2[0] + "." + team_ip2[1:]

    elif len(team_ip2) == 4:
        team_ip2 = team_ip2[0:2] + "." + team_ip2[2:]


pc_test_mode = InputPFunctions.find_arg("--pc-test-mode", num=True)
test_mode = InputPFunctions.find_arg("--test-mode", num=True)
pc_mode = InputPFunctions.find_arg("--pc-mode", num=True)

if os.name == "nt":
    pc_mode = 1
    
if pc_mode is not None:
    skip_cam_arg = 1
    skip_nt_arg = 1

elif pc_test_mode is not None:
    pc_mode = 1
    skip_cam_arg = 1
    skip_nt_arg = 1
    test_mode = 1

else:
    skip_cam_arg = InputPFunctions.find_arg("--skip-camera-check", num=True)
    skip_nt_arg = InputPFunctions.find_arg("--skip-network-check", num=True)

# endregion

# DIKKAT
# Match mode otonom yuzunden diger tum menulerden farkli bir print
# fonksiyonuna ve getvalues'a ihtiyac duyuyor
# match mode icin get menu values fonksiyonu

def match_mode(stdscr, settings=None, led1=None, out1=None, swt1=None, pot1=None, PanicMenu=False, errmsg=None):
    if not PanicMenu:
        led_control = {}
        # Ana yer
        while True:
            #Dosyadan okumayi dene
            led_control = DbFunctions.get_setting(file_lc) # led control dosyasindan ayari cekiyor
            if handle_error(led_control, stdscr, PanicMenu=False):
                led_control = {}
                led_control["status"] = True
           
            m_menu_elements = [] # Menu elementleri arrayi
            m_menu_elements.append(" ## MATCH MODE STARTED ## ") # Title

            # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
            if led_control["status"] is not None and led_control["status"] in [True, False, "True", "False"]:
                m_menu_elements.append(" ## LED CONTROL : " + str(led_control["status"]) + " ## ")


            # Eger kapali yada acik alamazsa error veriyor.
            else:
                m_menu_elements.append(" ## LED CONTROL FAILED ## ")
                led_control["status"] = True


            # Menunun geri kalani, durum reporu veriyor.
            m_menu_elements.append(" ## CAMERA_TOLERANCE : " + str(settings["Camera Tolerance"]) + " ## ")
            m_menu_elements.append(" ## ROBOT_LOCATION : " + str(settings["Robot Location"]) + " ## ")
            m_menu_elements.append(" ## WAITING_PERIOD : " + str(settings["Waiting Period"]) + " ## ")
            m_menu_elements.append(" ## AUTONOMOUS_MODE : " + str(settings["Autonomous Mode"]) + " ## ")


            if led_control["status"] in ["True", True]:
                ArduinoFunctions.led_write(led1, out1 , 1) # on

            elif (led_control["status"] in ["False", False]):
                ArduinoFunctions.led_write(led1, out1, 0) # off

            else:
                ArduinoFunctions.led_write(led1, out1, 1) # on


            print_menu_for_match(stdscr, m_menu_elements)


            # Exit kodu
            if (
                ArduinoFunctions.map_xi(pot1.read(), 0, 1, 0, max_v) == max_v
                and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == 0
            ):
                ArduinoFunctions.led_write(led1, out1 , 1) # on
                break
   
    ### KERNEL PANIC ###
    else:        
        settings = DbFunctions.get_setting(file_s)
        led_control = DbFunctions.get_setting(file_lc) # led control dosyasindan ayari cekiyor
        
        if handle_error(led_control, stdscr, PanicMenu=False) or handle_error(settings, stdscr, PanicMenu=False):
            led_control = {}
            led_control["status"] = True
            
            settings = {}
            settings[setting_names[0]] = setting_defaults[0]
            settings[setting_names[1]] = setting_defaults[1]
            settings[setting_names[2]] = setting_defaults[2]
            settings[setting_names[3]] = setting_defaults[3]
            settings[setting_names[4]] = setting_defaults[4]          
        
        m_menu_elements = [] # Menu elementleri arrayi
        m_menu_elements.append(" ## PANIC MODE STARTED ## ") # Title

        # LED Bilgisayar tarafindan kontrol ediliyor ve menu bunu gosteriyor
        if led_control["status"] is not None and led_control["status"] in [True, False, "True", "False"]:
            m_menu_elements.append(" ## LED CONTROL : " + str(led_control["status"]) + " ## ")


        # Eger kapali yada acik alamazsa error veriyor.
        else:
            m_menu_elements.append(" ## LED CONTROL FAILED ## ")
            led_control["status"] = True
            rv = DbFunctions.save_settings(file_lc, led_control) # Olmazsa yapacak bir şey yok
            handle_error(rv, stdscr, PanicMenu=False)

        if settings is not None:    
            # Menunun geri kalani, durum reporu veriyor.
            try:
                m_menu_elements.append(" ## CAMERA_TOLERANCE : " + str(settings["Camera Tolerance"]) + " ## ")
                m_menu_elements.append(" ## ROBOT_LOCATION : " + str(settings["Robot Location"]) + " ## ")
                m_menu_elements.append(" ## WAITING_PERIOD : " + str(settings["Waiting Period"]) + " ## ")
                m_menu_elements.append(" ## AUTONOMOUS_MODE : " + str(settings["Autonomous Mode"]) + " ## ")
            except:
                pass
        
        errortimer = threading.Timer(5, print_error, args=[stdscr, None])
        errortimer.start()
        print_error(stdscr, errmsg)

        while True:    
            print_menu_for_match(stdscr, m_menu_elements)
            
            if type(errmsg) == str and errmsg.startswith("InputP"):
                print_info(stdscr, errmsg, color=2, time=5)
                errmsg = None
                
            background_setup(stdscr, None, PanicMode=True)
            time.sleep(30)
            
            


def get_first_menu_values():
    ipaddr_func = InputPFunctions.get_ipaddr()
    check_cam_func = InputPFunctions.check_cam()

    mainmenu = []
    mainmenucheck = []

    if skip_nt_arg is not None:
        mainmenu.append("SKIPPED NETWORK CHECKING")
        mainmenucheck.append(True)

    elif ipaddr_func.startswith("127"):
        mainmenu.append("IP ADRESS: NOT CONNECTED")
        mainmenucheck.append(False) ## False

    elif not ipaddr_func.startswith("10." + team_ip2):
        mainmenu.append("NOT CONNECTED TO RADIO")
        mainmenucheck.append(False) ## False

    else:
        mainmenu.append("IP ADRESS: " + ipaddr_func)
        mainmenucheck.append(True)


    mainmenu.append("ARDUINO CONFIG")
    mainmenucheck.append(True)

    if skip_cam_arg is not None:
        mainmenu.append("SKIPPED CAMERA CHECKING")
        mainmenucheck.append(True)

    elif check_cam_func == "CAMERA.PY CONNECTED" or check_cam_func == "TRUE BECAUSE WINDOWS":
        mainmenu.append(check_cam_func)
        mainmenucheck.append(True)

    else:
        mainmenu.append(str(check_cam_func))
        mainmenucheck.append(False) ## False

    mainmenu.append("LED TEST")
    mainmenucheck.append(True)

    mainmenu.append("INFO")
    mainmenucheck.append(True)

    mainmenu.append("EXIT")
    mainmenucheck.append(True)

    return [mainmenu, mainmenucheck]


def get_ip_menu_values(ssid_func=InputPFunctions.get_ssid(), ipaddr_func=InputPFunctions.get_ipaddr()):
    mainmenu = []
    mainmenu_status = []

    if skip_nt_arg is not None:
        mainmenu.append(" ## SKIPPED NETWORK CHECKING ## ")
        mainmenu_status.append(False)

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

    elif not ipaddr_func.startswith("10." + team_ip2):
        mainmenu_status.append(False)
        mainmenu_status.append(False)

    else:
        mainmenu_status.append(True)
        mainmenu_status.append(True)

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

    mainmenu.append("RETURN TO MAIN MENU")
    mainmenu_status.append(False)

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


def get_info_menu_values(teamnumber):
    menu = []
    menucheck = []

    menu.append("MADE FOR FRC 2020 SEASON")
    menucheck.append(True)

    menu.append("Made by:")
    menucheck.append(True)

    menu.append("TUNAPRO123")
    menucheck.append(True)

    menu.append("ColonelKai")
    menucheck.append(True)

    menu.append("BlackShadow")
    menucheck.append(False)

    return [menu, menucheck]


def print_info(stdscr, input_str, color=2, time=5):
    errortimer = threading.Timer(time, print_error, args=[stdscr, None])
    errortimer.start()
    print_error(stdscr, input_str, color=color)


def print_error(stdscr, cur_stat, color=2):
    if type(cur_stat) == str:
        errmsg = cur_stat
        if errmsg is not None:
            h, w = stdscr.getmaxyx()
            x = w // 2 - (len(errmsg) + 1) // 2
            y = h - 1
            stdscr.attron(curses.color_pair(color))
            stdscr.addstr(y, x, errmsg)
            stdscr.attroff(curses.color_pair(color))
            stdscr.refresh()

    elif cur_stat is not None:
        errmsg = cur_stat["current_error"]
        if errmsg is not None:
            h, w = stdscr.getmaxyx()
            x = w // 2 - (len(errmsg) + 1) // 2
            y = h - 1
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, errmsg)
            stdscr.attroff(curses.color_pair(2))
            stdscr.refresh()

    elif cur_stat is None:
        h, w = stdscr.getmaxyx()
        x = (w // 2) - (1 // 2)
        y = h - 1
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(y, x, "")
        stdscr.attroff(curses.color_pair(2))
        stdscr.refresh()


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

    teamname = "FRC7839 "
    namex = w - len(teamname)
    namey = 0

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(namey, namex, teamname)
    stdscr.attroff(curses.color_pair(3))

    stdscr.refresh()


def print_menu_for_match(stdscr, m_menu_elements):
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


def set_current_menu(cur_stat, all_menu_elements):
    cur_menu = int(cur_stat["current_menu"])
    
    cur_stat["current_menu_elements"] = all_menu_elements[cur_menu][0]
    cur_stat["current_menu_status"] = all_menu_elements[cur_menu][1]
    
    return cur_stat["current_menu_elements"], cur_stat["current_menu_status"]


def return_to_menu(key, cur_stat):
    # Ana Menuye Cikma
    if (
        (key == "button0")
        and cur_stat["current_menu"] != 0
        and cur_stat["current_row"] == (len(cur_stat["current_menu_elements"]) - 1)
    ):
        cur_stat["current_row"] = 0
        cur_stat["current_menu"] = 0

    # Save settings icin
    if (
        (key == "button0")
        and cur_stat["current_menu"] == arduino_menu_value
        and cur_stat["current_row"] == (len(cur_stat["current_menu_elements"]) - 2)
    ):
        cur_stat["current_row"] = 0
        cur_stat["current_menu"] = 0
    

    return cur_stat["current_row"], cur_stat["current_menu"]


def background_setup(stdscr, cur_stat=None, PanicMode=False):
    if PanicMode == True:
        stdscr.bkgd(" ", curses.color_pair(2))
        
    elif cur_stat is not None and cur_stat["current_menu"] == 0:
        for i in cur_stat["current_menu_status"]:
            if i:
                stdscr.bkgd(" ", curses.color_pair(3))

            elif not i:
                stdscr.bkgd(" ", curses.color_pair(2))
                break

    elif cur_stat is not None and cur_stat["current_menu"] != 0:
        stdscr.bkgd(" ", curses.color_pair(4))
    

def refresh_screen(stdscr, cur_stat, settings):
    new_all_menu_elements = cur_stat["all_menu_elements"]


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


def handle_errors(stdscr=None, PanicMenu=True, *args):
    for variable in args:    
        if type(variable) == str:
            if str(variable).startswith("InputP"):
                background_setup(stdscr, None, PanicMode=True)
                
                if test_mode is not None:
                    raise Exception(str(variable))

                else:
                    if PanicMenu:
                        match_mode(stdscr, PanicMenu=True, errmsg=variable)
                    else:
                        print_info(stdscr, variable, color=2, time=5)
                    return True
            else:
                return False


def handle_error(variable, stdscr=None, PanicMenu=True):  
    if type(variable) == str:
        if str(variable).startswith("InputP"):
            background_setup(stdscr, None, PanicMode=True)
            
            if test_mode is not None:
                raise Exception(str(variable))

            else:
                if PanicMenu:
                    match_mode(stdscr, PanicMenu=True, errmsg=variable)
                else:
                    print_info(stdscr, variable, color=2, time=5)
                return True
        else:
            return False





def not_main(stdscr):
    # region while dongusune kadar olan gereksiz seyler

    #region Settings okuma
    settings = DbFunctions.get_setting(file_s)
    handle_error(settings, stdscr)
    #endregion

    all_menu_elements = []
    all_menu_elements.append(get_first_menu_values())
    all_menu_elements.append(get_ip_menu_values())
    all_menu_elements.append(get_arduino_menu_values(settings))
    all_menu_elements.append(get_cam_menu_values(None))
    all_menu_elements.append(get_info_menu_values(None))

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
        "all_menu_elements": all_menu_elements
    }


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

    msg = None
    key = None

    refresh_screen(stdscr, cur_stat, settings)

    # time.sleep(1)
    # region arduino import

    # board = pyfirmata.ArduinoNano("COM4")
    print_error(stdscr, "InputP INFO: Importing Arduino", 3)

    start_t = timeit.default_timer()
    ###

    com_ports = ArduinoFunctions.check_ports()
    
    if type(com_ports) == list:
        board = ArduinoFunctions.import_arduino(com_ports)
    
    else:
        board = all_errors[ARDUINO_CONN_ERR]
        
    ###
    elapsed = timeit.default_timer() - start_t
    
    if elapsed < 5:
        time.sleep(5 - elapsed)

    print_error(stdscr, None)
        
    if type(board) == str:
        handle_error(board, stdscr)
    
    else:
        print_info(stdscr, "InputP INFO: SUCCESSFUL", color=3, time=3)

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

    rv = ArduinoFunctions.led_write(led1, out1, 1.0)
    handle_error(rv, stdscr, PanicMenu=True)


    while True:

        ##########
        # Ekran yenilenmesi
        cur_stat["all_menu_elements"] = refresh_screen(stdscr, cur_stat, settings=settings)

        key, ports = ArduinoFunctions.key_get(but1, but2, pot1, wait_time_for_get_key, ArduinoFunctions.check_ports)
        handle_error(key, stdscr, PanicMenu=True)
        handle_error(ports, stdscr, PanicMenu=True)

        if ports, 

        # Imlec hareketleri degiskenlere yazildi
        cur_stat["current_row"] = cursor_handler(key, cur_stat)

        ##########

        for i in cur_stat["all_menu_elements"][main_menu_value][1]:
            if i:
                canGoToMM = True

            elif not i:
                canGoToMM = False
                break

        # Mac Modu
        if (
            canGoToMM == True
            and ArduinoFunctions.map_xi(pot1.read(), 0, 1, 0, max_v) == 0
            and ArduinoFunctions.map_xi(swt1.read(), 0, 1, 0, max_v) == max_v
            and cur_stat["current_menu"] == main_menu_value
        ):
            match_mode(stdscr, settings, led1, out1, swt1, pot1)

        
        
        
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

            # Write tusu
            if (
                key == "button0"
                and cur_stat["current_row"] == 4
            ):

                rv = DbFunctions.save_settings(file_s, settings)
                handle_error(rv, stdscr, PanicMenu=True)
                
                # if waiting_period is not None:
                #     DbFunctions.write_setting_to_txt(waiting_period, file)

            all_menu_elements[2] = get_arduino_menu_values(settings)

            cur_stat["current_menu_elements"] = all_menu_elements[2][0]
            cur_stat["current_menu_status"] = all_menu_elements[2][1]

        # endregion


        # Menu degistirme olaylari
        cur_stat["current_row"], cur_stat["current_menu"] = InputPFunctions.change_menu(key, cur_stat, led1, out1)
        cur_stat["current_row"], cur_stat["current_menu"] = return_to_menu(key, cur_stat)
        cur_stat["current_menu_elements"], cur_stat["current_menu_status"] = set_current_menu(cur_stat, all_menu_elements)


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
