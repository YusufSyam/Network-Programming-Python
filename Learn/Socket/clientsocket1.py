import socket

# menginput alamat socket
alamatServer= input("Masukkan alamat server > ")

# Mengaktifkan socket server
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Koneksi menuju alamat server
# Di sini portnya saya kasih sama dengan server
s.connect((alamatServer, 2120))

# Mengirim pesan
pesan= input("> ")

# Akan menghentikan program jika klien mengirim pesan 'bye'
while pesan!="bye":
    # Mengirim pesan yang diencode
    s.send(pesan.encode())

    # Menampung pesan yang dikirim oleh server ke variabel data
    data= ""
    for i in range(10):
        data+= s.recv(1024).decode()
        print(data)
    # while(data != ""):


    print("Server:",data)

    # Lanjut mengirim pesan ke server
    pesan= input("> ")
s.close()


