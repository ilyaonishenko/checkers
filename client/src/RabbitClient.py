import pika
import uuid
import json
import configparser
from pkg_resources import resource_filename
from client.src.Encoder import Encoder


class RabbitClient(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(resource_filename('server', 'foo.config'))
        self.uname = 'admin'
        self.pas = 'password'
        self.info = pika.PlainCredentials(self.uname, self.pas)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            '188.166.85.167', credentials=self.info))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        # 2802

    def call(self, n, name='rpc_queue'):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        cBody = json.dumps(n, cls=Encoder)
        # print(cBody)
        self.channel.basic_publish(exchange='',
                                   routing_key=name,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=cBody)
        while self.response is None:
            self.connection.process_data_events()
        # return hash(self.response)
        return json.loads(self.response.decode("utf-8"))

# fibonacci_rpc = FibonacciRpcClient()
#
# print(" [x] Requesting fib(30)")
# response = fibonacci_rpc.call(30)
# print(" [.] Got %r" % response)
