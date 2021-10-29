import socket #mengimpor socket

server_address=('localhost',5050) #menentukan alamat server
SIZE=1024 #menentukan ukuran buffer
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #membuat objek socket
s.connect(server_address) #menghubungkan socket ke alamat server

while True:
    pesan=s.recv(1024) #menerima pesan
    print ("Server :",pesan)  #pesan yang diterima dari server
    pesan= input("Anda : ").encode() #menginput pesan
    s.send(pesan) #mengirim pesan