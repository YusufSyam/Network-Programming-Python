from ftplib import FTP

ftp= FTP("localhost")
user= '' # Masukkan User
passwd= '' # Masukkan Password
ftp.login(user=user, passwd=passwd)

namaFile= input("Masukkan nama file yang ingin diupload: ")

with open(namaFile,"rb") as uploadFile:

    # Setelah data dibaca, maka dikirim
    ftp.storbinary("STOR "+namaFile, uploadFile)
    uploadFile.close()

print("Berhasil mengupload")

# Jalan upload file ini adalah
# Pertama tama mencari file di dalam folder yang sama dengan file python ini
# Lalu mengirimnya ke folder shared_folder di server