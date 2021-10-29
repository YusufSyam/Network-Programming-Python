"""
Mengimport module yang akan digunakan dalam program
"""
import select
import socket
import sys
import signal
import _pickle as cPickle
import struct
import argparse

# Server Host dengan 'localhost'
SERVER_HOST = 'localhost'

# mendefinisikan argumen
CHAT_SERVER_NAME = 'server'


def send(channel, *args):
    #membuat variabel baru untuk mengambil serialisasi data dari input
    buffer = cPickle.dumps(args)

    #konversi dari host byte ke network byte
    value = socket.htonl(len(buffer))

    #Mendefinisikan size dari argumen
    size = struct.pack("L", value)

    #mengirim data size ke socket yang lain
    channel.send(size)

    #mengirim data buffer ke socket yang lain
    channel.send(buffer)


def receive(channel):
    #mengambil ukuran dari struct
    size = struct.calcsize("L")

    #mengubah objek size ke byte
    size = channel.recv(size)
    try:
        # Mengubah ke 32bit atau 4byte
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error:
        return ''
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return cPickle.loads(buf)[0]


"""
class server yang akan digunakan untuk mendefenisikan fungsi fungsi yang digunakan dalam server
"""


class ChatServer(object):
    def __init__(self, port, backlog=5):
        # Mendefinisikan variabel pendukung
        self.clients = 0
        self.clientmap = {}
        self.outputs = []

        # mendefiniskan dan mengkonfigurasi server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Mengkonfigurasi socket dari server
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Mengikat server host dan port untuk digunakan sebagai bridge
        self.server.bind((SERVER_HOST, port))
        print('Server listening to port: %s ...' % port)
        # Tracking pada server terhadap backlog
        self.server.listen(backlog)
        # Mengatur signal untuk server
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        print('Shutting down server...')
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        # Mengambil data client yang baru saja join ke server
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        # untuk run maka harus run server, lalu client dan variabel
        # inputs akan menyimpan data dari client ke server
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        while running:
            try:
                # Mengambil data dari variable inputs untuk
                # di simpan ke variable readable dan yang lainnya
                readable, writeable, exceptional = \
                select.select(inputs, self.outputs,[])
            except select.error:
                break
            for sock in readable:
                # jika sock, sesuai dengan server
                if sock == self.server:
                    # Mengambil data client, dan alamat ipnya
                    client, address = self.server.accept()
                    print("Chat server: got connection %d from %s" %
                          (client.fileno(), address))
                    cname = receive(client).split('NAME: ')[1]
                    # menambah client, karena barusan ada yang masuk
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)
                    # menampilkan data sesuai client yang mengirim data
                    self.clientmap[client] = (address, cname)
                    msg = "\n(Connected: New client (%d) from %s)" %\
                    (self.clients, self.get_client_name(client))
                    for output in self.outputs:
                        # Sending message
                        send(output, msg)
                    # Output di tambah
                    self.outputs.append(client)
                # Jika sock sesuai dengan system
                elif sock == sys.stdin:
                    junk = sys.stdin.readline()
                    running = False
                else:
                    try:
                        # mengambil data dari sock
                        data = receive(sock)
                        # jika ada
                        if data:
                            msg = '\n#[' + self.get_client_name(
                                sock) + ']>>' + data
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)

                        else:
                            print("Chat server: %d hung up" % sock.fileno())
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            msg = "\n(Now hung up: Client from %s)" % self.get_client_name(
                                sock)
                            for output in self.outputs:
                                send(output, msg)
                    except socket.error:
                        inputs.remove(sock)
                        self.outputs.remove(sock)
        self.server.close()


"""
Mendefenisikan class Chat Client untuk client dalam aplikasi
"""


class ChatClient(object):
    def __init__(self, name, port, host=SERVER_HOST):
        # Mendefinisikan variabel, yang dibutuhkan
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.prompt = '[' + '@'.join(
            (name, socket.gethostname().split('.')[0])) + ']> '
        try:
            # Mengambil data socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # menconnect socket yang diterima
            self.sock.connect((host, self.port))
            print("Now connected to chat server@ port %d" % self.port)
            self.connected = True
            # Mend send nama dari client ke server
            send(self.sock, 'NAME: ' + self.name)
            # Mengambil data dari socket
            data = receive(self.sock)
            addr = data.split('CLIENT: ')[1]
            # Membuat perintah
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error:
            print("Failed to connect to chat server @ port %d" % self.port)
            sys.exit(1)

    def run(self):
        while self.connected:
            try:
                # Memprint data dari variable prompt
                sys.stdout.write(self.prompt)
                # output di bersihkan
                sys.stdout.flush()
                readable, writeable, exceptional = select.select(
                    [0, self.sock], [], [])
                for sock in readable:
                    if sock == 0:
                        # Membaca data dari server
                        data = sys.stdin.readline().strip()
                        # Jika ada maka akan di send
                        if data: send(self.sock, data)
                    elif sock == self.sock:
                        # data dari sock di receive
                        data = receive(self.sock)
                        if not data:
                            print('Client shutting down.')
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                # Jika ada tindis sembarangan
                print(" Client interrupted. ")
                self.sock.close()
                break


# Jalankan program seperti biasanya
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port',
                        action="store",
                        dest="port",
                        type=int,
                        required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name
    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()
