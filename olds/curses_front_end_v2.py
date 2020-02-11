from pyfirmata.util import Iterator 
import curses_functions
import pyfirmata
import ipaddress
import curses
import socket
import time
import zmq
import os

#Eğer ip adresimiz 10.78.39. ile başlıyorsa RADIO CONNECTED yazsın 

###################################################################################################
# Kullanım:                                                                                       #
#                                                                                                 #
# Menu 1'deki değerler:                                                                           #
# IP Addresi, Kamera Bağlı mı, Arduino Bağlı mı.                                                  #
#                                                                                                 #
# Menu 1 Değerleri Ayarlama:                                                                      #
# menuOneSetValues( IP ADRESİ, KAMERA BAĞLI MI, ARDUINO BAĞLI MI)                                 #
# IP adresi yok ise "" olarak koy.                                                                #
# Kamera ve Arduino Boolean değerler                                                              #
# Uyarı, değerleri def menuOneSetValues'den sonra yapmayı unutma.                                 #
################################################################################################### #Kullanım

# Row değiştirme pot (done)
# Ana menü exit eklenecek (done)
# Arduino menüye send eklenecek (done)
# Background değişimi
# Server client ekleme


def sendValuesToCamera(robo_loc):
    tcp_port = 5800
    settings = []
    settings = curses_functions.addSetting("isTest", "True", settings)
    settings = curses_functions.addSetting("robot_location", robo_loc, settings)
    
    status = curses_functions.transmit_settings(settings, tcp_port)
    return status

def check_cam():
    return False

def check_arduino():
    return True

def get_ipaddr(hostname = socket.gethostname()):
    ipaddr = socket.gethostbyname(socket.gethostname()) 
    return ipaddr

def get_ssid():
    return "Deneme"

def menuOneGetValues(ipaddr_func = get_ipaddr(), check_cam_func = check_cam(), check_arduino_func = check_arduino()):
    mainmenu = []
    mainmenucheck = []
    if ipaddr_func == "127.0.0.1": 
        mainmenu.append("IP ADRESS: NOT CONNECTED")
        mainmenucheck.append(False)
    else:
        mainmenu.append("IP ADRESS: " + ipaddr_func)
        mainmenucheck.append(True)
    if check_arduino_func:
        mainmenu.append("ARDUINO CONFIG")
        mainmenucheck.append(True)
    if check_cam_func:
        mainmenu.append("CAMERA CONNECTED")
        mainmenucheck.append(True)
    elif not check_cam_func:
        mainmenu.append("CAMERA NOT CONNECTED")
        mainmenucheck.append(False)
        
    mainmenu.append("EXIT")
    mainmenucheck.append("Normal")
    
    return [mainmenu, mainmenucheck]

def menuIpGetValues(ssid_func = get_ssid(), ipaddr_func = get_ipaddr()):
    mainmenu = []
    mainmenu_status = []
    mainmenu.append("HOSTNAME: " + str(socket.gethostname()))
    mainmenu.append("SSID: " + str(ssid_func))
    mainmenu.append("IP ADRESS: " + ipaddr_func)
    mainmenu.append("OK")
   
    mainmenu_status.append("Normal")
    
    if ipaddr_func == "127.0.0.1":
        mainmenu_status.append(False)
        mainmenu_status.append(False)
        mainmenu[2] = "IP ADRESS: NOT CONNECTED"
    else:
        mainmenu_status.append("Normal")
        mainmenu_status.append("Normal")
    
    mainmenu_status.append("Normal")
    
    return [mainmenu, mainmenu_status]
    
def menuArduinoGetValues(robo_loc = None):
    mainmenu = []
    mainmenu_status = []
    if robo_loc == None:
        mainmenu.append("WAITING FOR INPUT")
        mainmenu_status.append(False)
    else:
        mainmenu.append("ROBOT LOCATION: " + robo_loc)
        mainmenu_status.append("Normal")
        
    mainmenu.append("SEND CURRENT SETTINGS")
    mainmenu_status.append("Normal")    
        
    mainmenu.append("OK")
    mainmenu_status.append("Normal"),
    
    return [mainmenu, mainmenu_status]

def print_menu(stdscr, selected_row_idx, mainmenu, mainmenu_status):
    if type(mainmenu[0]) is list:
        mainmenu = mainmenu[0]
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(mainmenu):
        if mainmenu_status[idx]:
            colornumber = 3
        elif not mainmenu_status[idx]:
            colornumber = 2 
        else:
            colornumber = 4

        x = w//2 - len(row)//2
        y = h//2 - len(mainmenu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.attron(curses.color_pair(colornumber))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(colornumber))
    stdscr.refresh()
        

def not_main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    all_menu_elements = []
    all_menu_elements.append(menuOneGetValues())
    all_menu_elements.append(menuIpGetValues()) 
    all_menu_elements.append(menuArduinoGetValues())
    
    # all_menu_elements[0] = mainmenu, [1] = ip, [2] = arduino
 
    #region arduino
    
    board = curses_functions.import_arduino()
    
    swt1 = board.get_pin("a:1:i")
    pot1 = board.get_pin("a:2:i")
    inp1 = board.get_pin("a:6:i")
    inp2 = board.get_pin("a:7:i")
    but1 = board.get_pin("d:2:i")
    but2 = board.get_pin("d:7:i")
    led1 = board.get_pin("d:11:p")
    iterator = Iterator(board)
    iterator.start()
    time.sleep(0.2)
    #endregion
    
    current_row = 0
    current_menu = 0
    
    print_menu(stdscr, current_row, all_menu_elements[0][0], all_menu_elements[0][1])
    current_menu_elements = all_menu_elements[0][0]
    current_menu_status = all_menu_elements[0][1]

    up = None
    down = None
    robo_loc = None
    
    # RENKLER
    # 2 = RED
    # 3 = GREEN
    # 4 = NORMAL
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True:  
        
        # Background şeysi
        if current_menu == 0:
            for i in current_menu_status:
                if i:
                    stdscr.bkgd(' ', curses.color_pair(3))
                elif not i:
                    stdscr.bkgd(' ', curses.color_pair(2))
                    break
                
        elif current_menu != 0:
            stdscr.bkgd(" ", curses.color_pair(4))
            
        print_menu(stdscr, current_row, current_menu_elements, current_menu_status)
                          
        key = curses_functions.whichIsChanged(but1, but2, pot1)
        
        #İmleç Aşağı
        if ((key == "button1") and (current_row < (len(current_menu_elements)-1))):
            current_row += 1
        #İmleç Döngü
        elif current_row == (len(current_menu_elements) - 1) and (key == "button1"):
            current_row = 0
        # Menü değiştirme  
        if (key == "button0") and current_row == 0 and current_menu == 0:
            current_menu = 1
            current_row = 0
        # Menü değiştirme
        elif (key == "button0") and current_row == 1 and current_menu == 0:
            current_menu = 2
            current_row = 0
          
        # arduino menü özel
        if current_menu == 2:
            if key != "button1" and key != "button0" and current_row == 0:
                robo_loc = key
                
                
            
            all_menu_elements[2] = menuArduinoGetValues(robo_loc)
            current_menu_elements = all_menu_elements[2][0]
            current_menu_status = all_menu_elements[2][1]
            
        # Programı kapatmak için,
        if key == "button0" and current_menu == 0 and current_row == 3:
            exit()
            
        # Arduino Send butonu
        if key == "button0" and current_menu == 2 and current_row == 1 and robo_loc != None:
            send_func_msg = sendValuesToCamera(robo_loc)    

        # Ana Menüye Çıkma
        if (key == "button0") and current_menu != 0 and current_row == (len(current_menu_elements)-1):
            current_menu = 0   
            current_row = 0 

        if current_menu == 0:
            current_menu_elements = all_menu_elements[0][0]
            current_menu_status = all_menu_elements[0][1]
            
        elif current_menu == 1:
            current_menu_elements = all_menu_elements[1][0]
            current_menu_status = all_menu_elements[1][1]
        
        elif current_menu == 2:
            current_menu_elements = all_menu_elements[2][0]
            current_menu_status = all_menu_elements[2][1]
        

        print_menu(stdscr, current_row, current_menu_elements, current_menu_status)

curses.wrapper(not_main)

# def main():
#     try:
#         curses.wrapper(not_main)
#     except:
#         time.sleep(1)
#         print("An error occured restarting in 5 seconds...")
#         time.sleep(5)
#         main()
        
# if __name__ == "__main__":
#     main()