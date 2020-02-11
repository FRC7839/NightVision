from stfu import *

def main():
    socketcl = ServerFunctions.connect_serer(12345)
    message = "hello world"
    try:
        ServerFunctions.send1(socketcl, message)
    except:
        print("BUNU OKUYORSAN KAYRA GERİZEKALIDIR")
    else:
        print("shet")
        
    
if __name__ == "__main__":
    main()