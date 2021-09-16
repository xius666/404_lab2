#!/usr/bin/env python3
import socket
import time
import sys
#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024
#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip
def main():
    host = 'www.google.com'
    port = 80
    buffer_size = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as start:
        print("start proxy server")
        start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        start.bind((HOST, PORT))
        #set to listening mode
        start.listen(2)

        #continuously listen for connections
        while True:
            conn, addr = start.accept()
            remote_ip = get_remote_ip(host)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as end:
                print("connecting to google")
                end.connect((remote_ip , port))
                full_data = conn.recv(BUFFER_SIZE)
                end.sendall(full_data)
                end.shutdown(socket.SHUT_WR)
                #recieve data, wait a bit, then send it back
                data = end.recv(buffer_size)
                conn.sendall(data)
                conn.close()
                end.close()

if __name__ == "__main__":
    main()
