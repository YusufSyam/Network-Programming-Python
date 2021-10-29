import sys
from ftplib import FTP

print("Menampilkan isi file di direktori FTP server")

# Pertama kita masukkan alamat, username dan password
alamat= input("Masukkan alamat FTP Server > ")
username= input("Masukkan username > ")
password= input("Masukkan password > ")

# Membuat variabel FTP yang mrngikat alamat
ftp= FTP(alamat)

# Login dengan username & password sebelumnya
# Untuk parameter password memang agak aneh, bukannya password malah passwd
ftp.login(user=username, passwd=password)

# Sebelum menampilkan isi file, kita harus membuat list kosong terlebih dahulu untuk menampung file2
daftarFile= []

# Memperlihatkan semua data di ftp server, kemudian ditampung di list daftarFile
ftp.dir(daftarFile.append)

# Sekarang daftarFile telah terisi
# Sekarang kita akan cek satu persatu isi dari daftarFile

print("\nDaftar isi file: ")
for isi in daftarFile:
    # Print isi daftarFile per line
    print(isi)
