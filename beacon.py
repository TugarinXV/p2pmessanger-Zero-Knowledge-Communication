import zmq

port = "8001"
context = zmq.Context()
beacon = context.socket(zmq.REP)
beacon.bind(f"tcp://*:{port}")
available_ports = ["5556", "5557", "5558", "5559", "5560"]
connected_users = []

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
    message = beacon.recv_string(zmq.NOBLOCK)
    try:
        if message:
            user_id, user_port = message.split('|')
            if user_id not in connected_users:
                connected_users.append(user_id)  # Добавление пользователя в список подключённых
                print(f"Новый пользователь {user_id} подключён на порту {user_port}")
            
            # Отправка списка портов, исключая порт текущего пользователя
            ports_to_send = [port for port in available_ports if port != user_port]
            beacon.send_json(ports_to_send)
    except zmq.Again:
        pass  # Нет входящих сообщений
        # Здесь можно добавить логику проверки онлайн-статуса портов
        # ...

# Запуск маяка на порту 9999
beacon(9999, available_ports)
