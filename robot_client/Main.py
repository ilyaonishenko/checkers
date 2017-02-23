import socket
import time
import pika
import configparser
from pkg_resources import resource_filename

config = configparser.ConfigParser()
config.read(resource_filename('server', 'foo.config'))
uname = config['RABBITMQ']['user']
pas = config['RABBITMQ']['password']
info = pika.PlainCredentials(uname, pas)
connection = pika.BlockingConnection(
pika.ConnectionParameters(host='188.166.85.167', credentials=info))
channel = connection.channel()

channel.queue_declare(queue='for_robot')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='for_robot',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()





