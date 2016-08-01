import redis
import threading
import time
import queue

conn = redis.Redis()
name = ''
mes_queue = queue.Queue()

def login():
    global name, conn
    name = input("Please input your nickname(Blank is not allowed): ")
    if conn.sismember("users", name):
        print("The user already exists, please rename!")
        login()
    else:
        conn.sadd("users", name)

def orderAnalyse():
    global name, conn
    while True:
        message = input("Chatroom> ")
        order_list = message.lower().split(' ')

        if order_list[0] == 'get':
            while not mes_queue.empty():
                print(mes_queue.get())
        elif order_list[0] == 'downline':
            conn.srem("users", name)
            print("Thank you")
            exit()
        elif order_list[0] == 'pub':
            mes_list = order_list[1:]
            message = ''
            for word in mes_list:
                message += (word + ' ')
            real_mes = name + ': ' + message 
            conn.publish("chat", real_mes.encode("utf-8"))
        elif order_list[0] == 'to':
            message = input(order_list[1] + "> ")
            real_mes = name + ': ' + message
            conn.publish(order_list[1], real_mes.encode("utf-8"))
        elif order_list[0] == 'users':
            users = conn.smembers("users")
            print(users)
        else:
            print("This command does not exist!")
            orderAnalyse()

def subPublic():
    global mes_queue, conn
    sub = conn.pubsub()
    sub.subscribe(["chat"])
    for msg in sub.listen():
        if msg['data'] == 1:
            pass
        else:
            mes_queue.put(msg['data'].decode('utf-8'))

def subPrivate():
    global mes_queue, conn, name
    sub = conn.pubsub()
    sub.subscribe([name])
    for msg in sub.listen():
        if msg['data'] == 1:
            pass
        else: 
            real_mes = '----------------------------------\n' +\
                       "whisper!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" +\
                       msg['data'].decode('utf-8') + '\n' +\
                       '----------------------------------'
            mes_queue.put(real_mes)



def run_client():
    login()
    subPub_thread = threading.Thread(target = subPublic)
    subPri_thread = threading.Thread(target = subPrivate)
    subPub_thread.setDaemon(True)
    subPub_thread.start()
    subPri_thread.setDaemon(True)
    subPri_thread.start()
    time.sleep(3)
    orderAnalyse()


if __name__ == '__main__':
    run_client()
