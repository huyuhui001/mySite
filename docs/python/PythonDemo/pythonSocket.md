### File server.py
```
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
```

### client.py
```
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9001))

while True:
    message = input("Please input message: ")
    client_socket.send(message.encode('UTF-8'))
```
### Demo
Start server   
```
# python3 server.py
```
Start multi-clients and send messages via each client   
```
# python3 client.py
```
