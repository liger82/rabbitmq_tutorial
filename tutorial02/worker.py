#!/usr/bin/env python
import pika
import time

'''
https://www.rabbitmq.com/tutorials/tutorial-two-python.html
'''


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

queue_name = 'task_queue'
# durable=True : rabbitmq를 다시 시작해도 작업을 유지할 수 있다.
channel.queue_declare(queue=queue_name, durable=True)
print(f' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f' [x] Received {body.decode()}')
    # 일부러 딜레이 상황을 주었다. 너무 빨리 진행되니깐 연산이 되는 척 하려고
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # 
    ch.basic_ack(delivery_tag=method.delivery_tag)

'''
2개 이상의 worker를 사용할 때, 주어지는 task마다 경중이 다를 수 있기 때문에 
무조건 worker에 순서대로 배치하는 것이 아니라
이전 메세지를 처리하고 확인할 때까지 새 메세지를 worker에게 보내지 않게 할 수 있다.
prefetch_count=1 : 한번에 하나의 메세지만 보내고 일을 하고 있으면 보내지말고 다른 여유로운 worker에게 작업 보내라는 의미
'''
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()