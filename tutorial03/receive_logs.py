#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# queue name을 지정하지 않을 경우 서버가 임의의 이름을 선택한다.
# exlusive=True : consumer 연결이 끊기면 큐를 삭제
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
print(f'queue_name : {queue_name}')

# exchange와 queue 간 관계
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(on_message_callback=callback,
                      queue=queue_name,
                      auto_ack=True)

channel.start_consuming()