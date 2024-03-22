import zmq
import threading
import json
import uuid

class Client():
    def __init__(self, filename="ports.json"):
        self.context = zmq.Context()
        
        self.other_ports = set()

        self.socket_send = self.context.socket(zmq.PUB)
        self.socket_send.bind("tcp://*:%s" % 0)

        self.socket_receive = self.context.socket(zmq.SUB)
        self.socket_receive.subscribe("")

        self.node_id = set()
        self.node_id = uuid.uuid4()

        self.ship = self.context.socket(zmq.REQ)
        self.ship.bind("tcp://*:%s" % 0)
        self.ship.connect(f"tcp://localhost:8001")
        self.endpoint = self.ship.getsockopt_string(zmq.LAST_ENDPOINT)
        self.my_port = self.endpoint.split(":")[-1]

        def req_ports_from_beacon():
            """функция для подключения к маяку за портами"""
            self.ship.send_string(f"{self.node_id}|{self.my_port}")
            spacing = self.ship.recv_json()
            spacing2 = json.loads(spacing)
            for port in spacing2:
                self.other_ports.add(port)


        def load_ports(filename="ports.json"):
            try:
                with open(filename, "r") as file:
                    self.other_ports = json.load(file)
                    return self.other_ports
            except FileNotFoundError:
                return set()

        def save_ports(ports, filename="ports.json"):
            with open(filename, "w") as file:
                json.dump(list(ports), file)

        if not self.other_ports:
            load_ports()
        else:
            req_ports_from_beacon()

        # блок для подключения к портам
        for p in self.other_ports:
            try:
                self.socket_receive.connect(f"tcp://localhost:{p}")
            except Exception as e:
                print("Exception: " + e)
                continue        
        save_ports()

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
                if self.socket_receive.recv_string() == "ilb&lbp(*p)b8Y78BR6_+bpb*yb(*by(b9":
                    self.ship.send_string(f"Daddy! i`m fine!{self.my_port}")
                else:
                    pass
                print(self.socket_receive,end="\n",flush=True)
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
