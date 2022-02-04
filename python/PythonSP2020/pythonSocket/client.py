#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9001))

while True:
    message = input("Please input message: ")
    client_socket.send(message.encode('UTF-8'))


