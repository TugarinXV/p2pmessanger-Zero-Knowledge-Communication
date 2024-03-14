from Client import Client

c = Client(5557,[5555, 5556], "C")
print("c Started")
c.send("Hello from c")
while True:
    print(flush=True)
    user_in = input(">> ")
    c.send("c said: " + user_in)