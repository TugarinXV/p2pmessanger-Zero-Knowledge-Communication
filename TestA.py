from Client import Client
a = Client(5555,[5556, 5557], "A")
print("A Started")
a.send("Hello from A")
while True:
    print(flush=True)
    user_in = input(">> ")
    a.send("A said: " + user_in)