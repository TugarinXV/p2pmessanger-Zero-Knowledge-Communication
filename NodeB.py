import zmq
import zmq.asyncio

context = zmq.asyncio.Context() #контейнер для соектов

async def pub_function(port_pub):
    '''подключение к сети в роли PUB паттерну PUB-SUB
    '''
    pub_socket = context.socket(zmq.PUB) # роль сокета
    pub_socket.bind(f"tcp://*:{port_pub}") # бинд сокета на хост
    
    global other_ports
    other_ports.add(port_pub) # добавление порта паба, в множество. чтобы остальные могли его слушать
    
    await pub_socket.send_string("подключён")


def sub2all():
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
port_pub = "5557"
# Порты PUB сокетов других узлов
other_ports = {"5555","5557", "5559"}

sub2all()
pub_function(port_pub)




# import zmq

# context = zmq.Context()
# host = "localhost"
# port = "5001"
# # Сокет для приема сообщений
# receiver = context.socket(zmq.SUB)
# receiver.connect(f"tcp://{host}:{port}")
# receiver.subscribe("")
# print("ПОДКЛЮЧЕНО")
# print(receiver.recv_string())




# while True:
#     # Ждем сообщения от NodeA
#     msg = receiver.recv_string()
#     print(f"собеседник: {msg.decode()}")

#     # Отправляем ответ NodeA
#     receiver.send(input("ПИШИ: ").encode())
#     print("sent")

#     time.sleep(1)