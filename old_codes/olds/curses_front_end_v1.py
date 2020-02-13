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

# Menu One Global Values:

def check_cam():
    return True

def check_arduino():
    return True

def get_ipaddr(hostname = socket.gethostname()):
    ipaddr = socket.gethostbyname(socket.gethostname()) 
    return ipaddr

def get_ssid():
    return "Deneme"

def menuOneGetValues(ipaddr_func = get_ipaddr(), check_cam_func = check_cam(), check_arduino_func = check_arduino()):
    mainmenu = []
    if ipaddr_func == "127.0.0.1": 
        mainmenu.append("IP Adress: Not Connected")
    else:
        mainmenu.append("IP Adress: " + ipaddr_func)
    if check_arduino_func:
        mainmenu.append("Arduino Connected")
    elif not check_arduino_func:
        mainmenu.append("Arduino Not Connected")
    if check_cam_func:
        mainmenu.append("Camera Connected")
    elif not check_cam_func:
        mainmenu.append("Camera Not Connected")
    
    return mainmenu 

def menuIpGetValues(ssid_func = get_ssid(), ipaddr_func = get_ipaddr()):
    mainmenu = []
    mainmenu.append("HOSTNAME: " + str(socket.gethostname()))
    mainmenu.append("SSID: " + str(ssid_func))
    mainmenu.append("IP ADRESS: " + ipaddr_func)
    mainmenu.append("OK")
    return mainmenu
    
def menuArduinoGetValues(robo_loc = None):
    mainmenu = []
    if robo_loc == None:
        mainmenu.append("BUNU OKUYORSAN SIYABEND GERIZEKALIDIR")
    else:
        mainmenu.append("ROBOT LOCATION: " + robo_loc)
    mainmenu.append("OK")
    return mainmenu

# Prints the menu

def print_menu(stdscr, selected_row_idx, mainmenu):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(mainmenu):
        x = w//2 - len(row)//2
        y = h//2 - len(mainmenu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()
        
def return_to_main_menu(current_menu, current_row, current_menu_elements, key):
    if (key == "button0") and current_menu != 0 and current_row == (len(current_menu_elements)-1):
        current_menu = 0   
        current_row = 0 
        return current_menu, current_row
    else:
        return current_menu, current_row

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
    
    print_menu(stdscr, current_row, all_menu_elements[0])
    current_menu_elements = all_menu_elements[0]
    
    up = None
    down = None
    

    while True:        
        key = curses_functions.whichIsChanged(but1, but2, pot1)
        
        #İmleç Aşağı
        if ((key == "button1") and (current_row < (len(current_menu_elements)-1))):
            current_row += 1
        #İmleç Döngü
        elif current_row == (len(current_menu_elements) - 1) and (key == "button1"):
            current_row = 0
        # Menü değiştirme  
        if (key == "button0") and current_row == 0:
            current_menu = 1
            current_row = 0
        # Menü değiştirme
        elif (key == "button0") and current_row == 1:
            current_menu = 2
            current_row = 0
          
          
        # Ana Menüye Çıkma
        current_menu, current_row = return_to_main_menu(current_menu, current_row, current_menu_elements, key)
        
        # arduino menü özel
        if current_menu == 2:
            if key != "button1" and key != "button0":
                robo_loc = key
            
            elif key != None:
                robo_loc = "WAITING_FOR_INPUT"
            
            all_menu_elements[2] = menuArduinoGetValues(robo_loc)
            current_menu_elements = all_menu_elements[2]


        if current_menu == 0:
            current_menu_elements = all_menu_elements[0]
        elif current_menu == 1:
            current_menu_elements = all_menu_elements[1]
        elif current_menu == 2:
            current_menu_elements = all_menu_elements[2]
        
        print_menu(stdscr, current_row, current_menu_elements)

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