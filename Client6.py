from socket import*

HOST = '192.168.41.1'
PORT = 9999
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    message = raw_input()  #client's message to the server
    s.send(message) #sends message to the server
    print("Waiting for response...")
    reply = s.recv(1024) #receives message from server
    print("New message: " + repr(reply)) #prints the message received

close()