import redis

# 服务器端。
conn = redis.Redis()


def pub():
    global conn
    while True:
        message = input("Please input message: ")
        real_mes = '\n----------------------------------\n' +\
                   'NOTEING!!!!!!!!!!!!!!!!!!!!!!!!!!!\n' +\
                   'Administrator say: ' + message + '\n' +\
                   '----------------------------------'
        conn.publish("chat", real_mes.encode("utf-8"))

if __name__ == '__main__':
    pub()
