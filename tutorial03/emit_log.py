#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# exchange 선언
# exchange 유형은 direct, topic, headers, fanout
# fanout : exchange에 연결된 모든 큐에 브로드캐스트함
# logs라는 이름으로 로그 메세지를 발생한다.
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# routing_key에 지정된 이름으로 큐가 존재하면 라우팅함
# fanout일 경우는 routing_key는 무의미 모두에게 보내서.
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()