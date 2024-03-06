import zmq
import time
from cipher import encrypt_message,decrypt_message
context = zmq.Context()

# Сокет для отправки сообщений
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5555")

# Сокет для приема ответов
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5556")

# Отправляем сообщение узлу B
print("Отправка сообщения узлу B...")
sender.send("Привет от A!".encode())

# Ждем ответа от узла B
message = receiver.recv()
print(f"Получен ответ от узла B: {message.decode()}")

time.sleep(1)  # Имитация задержки
