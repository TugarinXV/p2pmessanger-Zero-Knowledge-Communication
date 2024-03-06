import zmq

context = zmq.Context()

# Сокет для приема сообщений
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5556")

# Сокет для отправки ответов
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5555")

# Ждем сообщения от узла A
message = receiver.recv()
print(f"Получено сообщение от узла A: {message.decode()}")

# Отправляем ответ узлу A
print("Отправка ответа узлу A...")
sender.send(b"Привет от B!")

