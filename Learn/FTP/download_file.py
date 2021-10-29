from ftplib import FTP

ftp= FTP("localhost")
# ftp.login(user=input("User: "), passwd=input("Password: "))
user= '' # Masukkan User
passwd= '' # Masukkan Password
ftp.login(user=user, passwd=passwd)

print("Daftar File di direktori")

daftarFile= []
ftp.dir(daftarFile.append)

print("\nDaftar isi file: ")
for isi in daftarFile:
    print(isi)

pilihFile= input("Pilih file untuk didownload: ")

# Memulai proses mendownload file
# Kita open dengan mode write binary
with open(pilihFile,"wb") as localFile:
    bacafile = ftp.retrbinary("RETR "+pilihFile, localFile.write)
    if bacafile.startswith('226'):
        # Maksud dari 226 di sini adalah bahwa file tersebut telah selesai terdownload
        print("Download Selesai...")
        localFile.close()
    else:
        print("Terjadi error")

# Hasil download akan tersimpan bersamaan dengan direktori file ini
print("UWAU")
ftp.quit()