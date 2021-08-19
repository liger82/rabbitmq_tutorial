#!/usr/bin/env python
import pika
import sys

# 연결하고
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 큐 생성
queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)

# arbitrary messages from command line
# message = ' '.join(sys.argv[1:]) or "Hello World!"

for message in range(1, 101):
    # 큐를 보냄
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=str(message),
        properties=pika.BasicProperties(
            delivery_mode=2, # make message persistant
        )
    )

    print(f" [x] Sent {message}")

connection.close()