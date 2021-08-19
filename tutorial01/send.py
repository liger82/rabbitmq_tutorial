# coding=utf-8
#!/usr/bin/env python

'''
출처: https://arisu1000.tistory.com/27770 [아리수]
https://www.rabbitmq.com/tutorials/tutorial-one-python.html
'''

import pika


# rabbitmq 연결
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# hello 큐를 생성, hello는 큐 이름
channel.queue_declare(queue='hello')

# hello 큐를 Hello World라는 메세지를 보냄
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print('Sent "Hello World!"')


connection.close()