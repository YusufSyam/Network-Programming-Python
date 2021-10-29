# Internet socket dengan tcp/ip
import socket

# Menyetel host
lokasi= socket.gethostbyname("127.0.0.1") # Atau bisa localhost

# Mengaktifkan server menggunakan standar alamat ipv4 lalu menyimpan dalam variabel s
# Parameter kedua adalah bentuk data yang terkirim
# socket.SOCK_STREAM untuk tcp, socket.SOCK_DGRAM untuk udp
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Membind (mengikat) host ke sebuah port, parameter ke dua adalah port
# Lokasi dan port harus berbentuk tuple, makanya berkurung 2
s.bind((lokasi, 2120))

# Listen atau menunggu koneksi, parameter pertama untuk menentukan jumlah maksimal klien/koneksi ke server
s.listen(2)

# Statement di bawah tidak akan tereksekusi kalau belum ada koneksi
print("Server sudah aktif!")

# Membuat client
client, alamat= s.accept()

# Memprint apabila telah menerima koneksi
print("Menerima koneksi dari",alamat)

# Proses mengirim pesan terjadi
while True:
    # parameter .recv() menentukan jumlah batas tampungan data
    data= client.recv(1024).decode()

    # Jika tak ada pesan masuk
    if not data:
        break

    # Memprint pesan dari klien
    print("Pesan masuk dari klien: ",str(data))

    # Server membalas
    kirim= input("> ")
    # if kirim == "": kirim = "kosong"
    client.send(kirim.encode())