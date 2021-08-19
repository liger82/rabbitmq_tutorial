#!/usr/bin/env python
import pika

'''
https://www.rabbitmq.com/tutorials/tutorial-six-python.html
'''

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_name = 'rpc_queue'
channel.queue_declare(queue=queue_name)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    n = int(body)

    response = fib(n)
    print(f" [.] fib({n}) = {response}")

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)

print(f' [x] Awaiting RPC requests')
channel.start_consuming()