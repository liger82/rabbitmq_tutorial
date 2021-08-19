#!/usr/bin/env python
import pika
import sys

'''
https://www.rabbitmq.com/tutorials/tutorial-five-python.html
'''

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

queue_name = 'topic_logs'
'''
direct는 1:1 매칭인데, topic은 1:N 매칭이 가능해서 더 유연한 binding rule을 사용할 수 있다.
'''
channel.exchange_declare(exchange=queue_name, exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonoymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange=queue_name,
    routing_key=routing_key,
    body=message
)

print(f' [x] Sent {routing_key}:{message}')
connection.close()