from stfu import ServerFunctions



def main():
    tcp_port = 12345
    socketsv = ServerFunctions.start_server(tcp_port)
    msg = ServerFunctions.recv1(socketsv, 2)

    print(msg)


if __name__ == "__main__":
    main()
