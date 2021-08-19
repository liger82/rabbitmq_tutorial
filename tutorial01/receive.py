# coding=utf-8
#!/usr/bin/env python

'''
출처: https://arisu1000.tistory.com/27770 [아리수]
https://www.rabbitmq.com/tutorials/tutorial-one-python.html
'''

import pika


# rabbitmq에 연결
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# hello 큐를 생성
channel.queue_declare(queue='hello')

# 큐에서 메세지를 받기 위한 콜백 함수
def callback(ch, method, properties, body):
    print(f"Received : {body}")

# 큐에서 지정한 콜백함수로 메세지 받기
channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

# 큐에서 답변이 올때까지 기다림.
print(f"[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()