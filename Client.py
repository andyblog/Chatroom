import redis
import threading
import time

#conn = redis.Redis()

name = ''

def login():
    global name
    name = input("Please input your nickname: ")

def pub():
    global name
    #global conn, name
    conn = redis.Redis()
    while True:
        message = input("Please input message: ")
        real_mes = '\n' + name + ': ' + message + '\n'
        conn.publish("chat", real_mes.encode("utf-8"))

def sub():
    #global conn
    conn = redis.Redis()
    sub = conn.pubsub()
    sub.subscribe(["chat"])
    for msg in sub.listen():
        if msg['data'] == 1:
            pass
        else:
            print(msg['data'].decode('utf-8'))


def run_client():
    login()
    sub_thread = threading.Thread(target = sub)
    sub_thread.start()
    time.sleep(3)
    pub()


if __name__ == '__main__':
    sub()
    #run_client()
