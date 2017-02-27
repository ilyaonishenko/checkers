import socket
import time
import pika
import configparser
import datetime
from pkg_resources import resource_filename


def send(message):
    last = datetime.datetime.now()
    td = (datetime.datetime.now() - last)
    if (td.seconds * 1000000 + td.microseconds * 200000):
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
uname = 'admin'
pas = 'grachevhuy'
info = pika.PlainCredentials(uname, pas)
connection = pika.BlockingConnection(pika.ConnectionParameters(
            '188.166.85.167', credentials=info))
channel = connection.channel()

channel.queue_declare(queue='for_robot')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    send(body.decode())

channel.basic_consume(callback,
                      queue='for_robot',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()





