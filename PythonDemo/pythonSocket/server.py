#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 9001))
server_socket.listen(1)  # 1代表监听线程的数量
print('waiting for connection...')


# function to receive message
def receive_message(sock, addr):
    while True:
        message = sock.recv(1024)
        print(message.decode('UTF-8'))


# accept request
while True:
    sock, addr = server_socket.accept()  # accept()的源码中return sock, addr
    print(sock, addr)
    # receive_message(sock, addr)  # receive message only from one client
    thread = threading.Thread(target=receive_message, args=(sock, addr))  # receive message from multi-clients
    thread.start()
