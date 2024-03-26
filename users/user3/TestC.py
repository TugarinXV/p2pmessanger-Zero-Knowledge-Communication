from Base.Client import Client

c = Client()
c.start_client()
print("c Started")
c.send("Hello from c")
while True:
    print(flush=True)
    user_in = input(">> ")
    c.send("c said: " + user_in)