from socket import*
import sys
import select

HOST = '192.168.41.1'
PORT = 8800
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    socket_list = [sys.stdin, s]

    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(
        socket_list, [], [])

    for sock in read_sockets:
        #incoming message from remote server
        if sock == s:
            data = sock.recv(1024)
            if not data:
                print('\nTerputus dari jaringan')
                break
            else:
                #print data
                sys.stdout.write(data)
                # prints the message received
                print("Klien: " + repr(data))
        #user entered a message
        else:
            msg = sys.stdin.readline()
            s.send(msg)
            prompt()