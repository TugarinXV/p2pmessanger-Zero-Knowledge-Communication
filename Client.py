

import zmq
import time
import threading

class Client():
    def __init__(self,port,other_ports):
        self.port = port
        self.context = zmq.Context()
        self.socket_send = self.context.socket(zmq.PUB)
        self.socket_send.bind(f"tcp://*:{self.port}")

        self.socket_receive = self.context.socket(zmq.SUB)
        self.socket_receive.subscribe("")


        for p in other_ports:
                try:
                    self.socket_receive.connect(f"tcp://localhost:{p}")
                    t = threading.Thread(target=self.recv)
                    t.daemon = True
                    t.start()
                except Exception as e:
                    print("Exception: " + e)
                    continue

    def send(self,message):
        try:
            self.socket_send.send_string(message)
        except zmq.ZMQError as zmq_error:
            print(f"SEND ZMQ Error: {zmq_error}")
        except Exception as e:
            print(f"SEND Error occurred: {e}")

    def recv(self):
        while True:
            try:
                msg = self.socket_receive.recv_string()
                print(msg,end="\n",flush=True)
            except zmq.ZMQError as zmq_error:
                print(f"RECV ZMQ Error: {zmq_error}")
            except Exception as e:
                print(f"RECV Error occurred: {e}")



# region test
# context = zmq.Context() #контейнер для сокетов

# def pub_function(port_pub,other_ports):
#     '''подключение к сети в роли PUB паттерну PUB-SUB
#     '''
#     pub_socket = context.socket(zmq.PUB) # роль сокета
#     pub_socket.bind(f"tcp://*:{port_pub}") # бинд сокета на хост
#     time.sleep(2)
    
#     other_ports.add(port_pub) # добавление порта паба, в множество. чтобы остальные могли его слушать
#     pub_socket.send_string("hello-pong")
#     return pub_socket


# def sub2all(port_pub):
#     '''функция саба на все узлы в сети'''
#     sub_socket = context.socket(zmq.SUB)
#     sub_socket.subscribe("") # подписался(в данном случае на всё
#     for port in other_ports: # можно сделать через filter() и лямбду. но пока мне в падлу
#         if port != port_pub:
#             sub_socket.connect(f"tcp://localhost:{port}") # подключился ко всем(кроме себя)
#     return sub_socket

# # Порт для PUB сокета текущего узла
# port_pub = "5555"
# # Порты PUB сокетов других узлов
# other_ports = {"5555","5557"}

# thread_list = [threading.Thread(target=sub2all, args=(port_pub,)), 
#                threading.Thread(target=sub2all, args=("5557",))]

# for t in thread_list: t.start(); t.join()
# time.sleep(1)
# sub_socket = pub_function(port_pub,other_ports)
# s = sub_socket.recv_string()
# print(s)
# endregion test
