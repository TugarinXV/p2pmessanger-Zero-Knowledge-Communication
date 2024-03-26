import zmq
import threading
import json
import uuid

class Client():
    def __init__(self, filename="ports.json"):
        self.context = zmq.Context()
        self.other_ports = set()
        self.node_id = str(uuid.uuid4())

        self.socket_send = self.context.socket(zmq.PUB)
        self.socket_send.bind("tcp://*:%s" % 0)

        self.socket_receive = self.context.socket(zmq.SUB)
        self.socket_receive.subscribe("")

        self.ship = self.context.socket(zmq.REQ)
        self.ship.connect(f"tcp://localhost:8001")
        self.endpoint = self.ship.getsockopt_string(zmq.LAST_ENDPOINT)
        self.my_port = self.endpoint.split(":")[-1]

    def start_client(self):
        self.load_ports()
        threading.Thread(target=self.recv, daemon=True).start()
        
        # блок для подключения к портам
        for p in self.other_ports:
            try:
                self.socket_receive.connect(f"tcp://localhost:{p}")
            except Exception as e:
                print("Exception: ", e)
                continue
        
        while True:
            user_input = input("Введите сообщение: ")
            self.send(user_input)

    def load_ports(self, filename="ports.json"):
        try:
            with open(filename, "r") as file:
                loaded_ports = json.load(file)
                self.other_ports.update(loaded_ports)
        except FileNotFoundError:
            self.req_ports_from_beacon()

    def req_ports_from_beacon(self):
        """Запрос портов у маяка и обновление self.other_ports"""
        self.ship.send_string(f"{self.node_id}|{self.my_port}")
        received_ports = self.ship.recv_json()
        self.other_ports.update(received_ports)
        self.save_ports()

    def save_ports(self, filename="ports.json"):
        with open(filename, "w") as file:
            json.dump(list(self.other_ports), file)

    def send(self, message):
        try:
            self.socket_send.send_string(message)
        except zmq.ZMQError as zmq_error:
            print("SEND ZMQ Error: ", zmq_error)
        except Exception as e:
            print("SEND Error occurred: ", e)

    def recv(self):
        while True:
            try:
                message = self.socket_receive.recv_string(zmq.NOBLOCK)
                print(f"Received: {message}")
            except zmq.Again:
                continue  # Продолжаем цикл, если нет сообщений
