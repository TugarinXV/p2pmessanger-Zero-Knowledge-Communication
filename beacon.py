import zmq
import time
import threading
import re

class Beacon:
    def __init__(self):
        self.context = zmq.Context()
        self.beacon = self.context.socket(zmq.REP)
        self.beacon.bind("tcp://*:8001")

        self.heart = self.context.socket(zmq.PUB)
        self.heart.bind("tcp://*:8002")

        self.socket_receive = self.context.socket(zmq.SUB)
        self.socket_receive.connect("tcp://localhost:8002")
        self.socket_receive.subscribe("")

        self.connected_users = []

    def start_beacon(self):
        heartbeat_thread = threading.Thread(target=self.heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

        while True:
            try:
                message = self.beacon.recv_string(zmq.NOBLOCK)
                if message:
                    user_id, user_port = message.split('|')
                    if user_port not in self.connected_users:
                        self.connected_users.append(user_port)
                        print(f"Новый пользователь {user_id} подключён на порту {user_port}")
                    
                    ports_to_send = [port for port in self.connected_users if port != user_port]
                    self.beacon.send_json(ports_to_send)
            except zmq.Again:
                pass

    def heartbeat(self):
        while True:
            self.heart.send_string("ilb&lbp(*p)b8Y78BR6_+bpb*yb(*by(b9")
            time.sleep(4)
            try:
                message = self.socket_receive.recv_string(zmq.NOBLOCK)
                match = re.search(r"Daddy! i`m fine!(\d+)", message)
                if match:
                    user_port = match.group(1)
                    if user_port not in self.connected_users:
                        self.connected_users.append(user_port)
                        print(f"Пользователь на порту {user_port} подключен.")
            except zmq.Again:
                pass
