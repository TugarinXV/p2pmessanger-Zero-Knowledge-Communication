from Client import Client
import time
b = Client(5556,[5555])
print("B Started")
b.send("Hello from b")

while True:
    print(flush=True)
    user_in = input(">> ")
    b.send("B said: " + user_in)