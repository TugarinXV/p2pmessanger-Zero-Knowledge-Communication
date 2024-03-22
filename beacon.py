import zmq
import time
import threading
import re

class Beacon():
    def __init__(self, connected_users: list):
        self.context = zmq.Context()
        
        self.beacon = self.context.socket(zmq.REP)
        self.beacon.bind(f"tcp://*:8001")
        self.heart = self.context.socket(zmq.PUB)
        self.heart.bind("tcp://*:8002")
        self.socket_receive = self.context.socket(zmq.SUB)
        self.socket_receive.subscribe("")

        def heartbeat():
            while True:
                self.heart.send_string("ilb&lbp(*p)b8Y78BR6_+bpb*yb(*by(b9\n")
                time.sleep(4)
                message = self.beacon.recv_string()
                if "Daddy! i`m fine!" in message:
                    regex = r"Daddy! i`m fine!(\d+)"
                    match = re.search(regex, message)
                    self.сonnected_users.append(match)

        heartbeat_thread = threading.Thread(target=heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

        # Функция для чтения события монитора
        def recv_monitor_message(monitor, flags=0, recv_timeout=1000):
            if monitor.poll(recv_timeout):
                msg = monitor.recv(flags)
                event = zmq.utils.monitor.parse_monitor_message(msg)
                return event
            else:
                raise zmq.Again()
            
        while True:
            # Ожидание подключения нового пользователя
            message = self.beacon.recv_string(zmq.NOBLOCK)
            try:
                if message:
                    user_id, user_port = message.split('|')
                    if user_id not in connected_users:
                        connected_users.append(user_id)  # Добавление пользователя в список подключённых
                        print(f"Новый пользователь {user_id} подключён на порту {user_port}")
                    
                    # Отправка списка портов, исключая порт текущего пользователя
                    ports_to_send = [port for port in connected_users if port != user_port]
                    self.beacon.send_json(ports_to_send)
            except zmq.Again:
                pass  # Нет входящих сообщений
                # Здесь можно добавить логику проверки онлайн-статуса портов


