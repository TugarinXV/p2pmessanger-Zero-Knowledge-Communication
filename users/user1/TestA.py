from Base.Client import Client
a = Client()
a.start_client()
print("A Started")
a.send("Hello from A")
while True:
    print(flush=True)
    user_in = input(">> ")
    a.send("A said: " + user_in)