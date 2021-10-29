from socket import*

HOST = ''
PORT = 9999

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
print("Now listening...")
s.listen(1)  # only needs to receive one connection (the client)
conn, addr = s.accept()  # accepts the connection
print("Connected by: ", addr)  # prints the connection
i = True

while i is True:

   data = conn.recv(1024)  # receives data
    print('Received:', repr(data))  # prints the message from client

    reply = raw_input()  # server types a response
    conn.sendall(reply)  # server now sends response back to client

close()