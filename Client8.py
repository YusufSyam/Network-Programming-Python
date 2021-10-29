from socket import*

HOST = '192.168.41.1'
PORT = 8800
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    message = raw_input("Chat: ")  #client's message to the server
    s.send(message) #sends message to the server
    print("Menunggu respon..")
    reply = s.recv(1024) #receives message from server
    print("Server: " + repr(reply)) #prints the message received

close()