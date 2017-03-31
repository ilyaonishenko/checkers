import socket
import time
import pika
import configparser
import datetime
from robot_client.Sender import *
from pkg_resources import resource_filename


def send(message):
    last = datetime.datetime.now()
    td = (datetime.datetime.now() - last)
    # if (td.seconds * 1000000 + td.microseconds * 200000):
    time.sleep(0.2)
    host = '10.0.0.2'
    port = 10002
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send((message + "\r\n").encode())
    buffer = 256
    resp = s.recv(buffer)
    s.close()
    print(resp)
    last = datetime.datetime.now()

config = configparser.ConfigParser()
config.read(resource_filename('server', 'foo.config'))
uname = 'admin3'
pas = 'grachevhuy3'
info = pika.PlainCredentials(uname, pas)
connection = pika.BlockingConnection(pika.ConnectionParameters(
            '188.166.85.167', credentials=info))
channel = connection.channel()

channel.queue_declare(queue='for_robot')

white_map = {-1: [20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 41, 42, 43]}
black_map = {-1: [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19]}

def startup():
    for i in range(0, 8):
        if i<3:
            a = 0
            if i%2 == 0:
                a = 1
            for j in range(a, 8, 2):
                tmp =  white_map[-1].pop(-1)
                num = Sender.reformat(j,i)
                white_map[num] = tmp
                send(Sender.start_move(tmp, num))
        elif i>4:
            a = 0
            if i % 2 == 0:
                a = 1
            for j in range(a, 8, 2):
                tmp = black_map[-1].pop(-1)
                num = Sender.reformat(j, i)
                black_map[num] = tmp
                send(Sender.start_move(tmp, num))

def cleanup():
    for i in white_map.keys():
        if(i == -1):
            continue
        placeto = white_map.pop(i)
        white_map[-1].append(placeto)
        send(Sender.remove(i, placeto))
    for i in black_map.keys():
        if(i == -1):
            continue
        placeto = black_map.pop(i)
        black_map[-1].append(placeto)
        send(Sender.remove(i, placeto))



def callback(ch, method, properties, body):
    print(" [x] Received %r" + body.decode())
    if body.decode() is "START_GAME":
        print("START_GAME")
        cleanup()
        startup()
    elif body.decode() is "CLEAN":
        print("CLEAN")
    else:
        pars = body.decode().split(' ')
        if(len(pars) == 1):
            placefrom = int(pars[0])
            if placefrom in white_map:
                placeto = white_map.pop(placefrom)
                white_map[-1].append(placeto)
            else:
                placeto = black_map.pop(placefrom)
                black_map[-1].append(placeto)
            send(Sender.remove(placefrom, placeto))
        else:
            placefrom, placeto = pars
            if placefrom in white_map:
                white_map[placeto] = white_map.pop(placefrom)
            else:
                black_map[placeto] = black_map.pop(placefrom)
            send(Sender.move(placefrom, placeto))




channel.basic_consume(callback,
                      queue='for_robot',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()





