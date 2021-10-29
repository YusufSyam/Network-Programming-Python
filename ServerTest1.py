import socket  # mengimport module socket

server_adress = ('localhost', 5050)  # menentukan alamat server
SIZE = 1024  # ukuran buffer ketika menerima pesan
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # membuat objek socket
s.bind(server_adress)  # meng-bind/mengikat ke alamat server
s.listen(5)  # menerima 6 koneksi (dari klien)

# menerima pesan terus menerus
while True:
    print("menunggu koneksi")
    client, client_adress = s.accept()  # menerima koneksi dari klien
    print("connected from : ", client_adress)
    while True:
        pesan = input("Anda : ").encode()  # memasukan pesan
        client.send(pesan)  # mengirim pesan ke klien
        pesan = client.recv(1024)  # menerima pesan dari klien
        print("client:", pesan)