import socket
import pika

if False:
    sock = socket.socket()
    sock.bind(('', 8080))

    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)

        if not data:
            continue
        print("Server received: " + str(data))

        conn.send(("MR GRACHEV IS A DEFINETELY HUY").encode())

    print('closed')
    conn.close()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    n = hash(body)

    print("want to send MR GRACHEV IS A DEFINETELY HUY")
    response = "MR GRACHEV IS A DEFINETELY HUY"

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
