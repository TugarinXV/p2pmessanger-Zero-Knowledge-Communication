import zmq

port = "8001"
context = zmq.Context()
beacon = context.socket(zmq.REP)
beacon.bind(f"tcp://*:{port}")


while True:
    # Ожидание подключения нового пользователя
    message = beacon.recv_string()
    if message == "REQUEST_PORTS":
        # Отправка 10 последних портов из списка доступных портов
        ports_to_send = available_ports[-10:]
        beacon.send_json(ports_to_send)

        # Здесь можно добавить логику проверки онлайн-статуса портов
        # ...

# Пример списка доступных портов
available_ports = [str(port) for port in range(5550, 5565)]

# Запуск маяка на порту 9999
beacon(9999, available_ports)
