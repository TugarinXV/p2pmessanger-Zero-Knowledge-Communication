from Base.Client import Client

b = Client()
b.start_client()
print("B Started")
b.send("Hello from b")
while True:
    print(flush=True)
    user_in = input(">> ")
    b.send("B said: " + user_in)
