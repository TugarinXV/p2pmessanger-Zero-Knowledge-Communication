
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time
import threading

context = zmq.Context() #контейнер для сокетов

def pub_function(port_pub):
    '''подключение к сети в роли PUB паттерну PUB-SUB
    '''
    pub_socket = context.socket(zmq.PUB) # роль сокета
    pub_socket.bind(f"tcp://*:{port_pub}") # бинд сокета на хост
    time.sleep(2)
    
    global other_ports
    other_ports.add(port_pub) # добавление порта паба, в множество. чтобы остальные могли его слушать
    
    pub_socket.send_string("подключён")


def sub2all(port_pub):
    '''функция саба на все узлы в сети'''
    sub_socket = context.socket(zmq.SUB)
    sub_socket.subscribe("") # подписался(в данном случае на всё)

    for port in other_ports: # можно сделать через filter() и лямбду. но пока мне в падлу
        if port != port_pub:
            sub_socket.connect(f"tcp://localhost:{port}") # подключился ко всем(кроме себя)

    while True:
        message = sub_socket.recv_string() # получение сообщений в str()
        
        print(f"получено: {message}")


# Порт для PUB сокета текущего узла
port_pub = "5555"

# Порты PUB сокетов других узлов
other_ports = {"5555","5557", "5559"}

sub_thread = threading.Thread(target=sub2all, args=(port_pub,))
sub_thread.start()
time.sleep(1)
print(pub_function(port_pub))
# #  Socket to talk to server
# print("Connecting to hello world server...")
# socket = context.socket(zmq.REQ)
# socket.connect("tcp://localhost:5555")

# #  Do 10 requests, waiting each time for a response
# for request in range(10):
#     print(f"Sending request {request} ...")
#     socket.send_string("Hello")

#     #  Get the reply.
#     message = socket.recv()
#     print(f"Received reply {request} [ {message} ]")
