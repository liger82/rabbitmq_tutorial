#!/usr/bin/env python
import pika
import uuid


'''
https://www.rabbitmq.com/tutorials/tutorial-six-python.html
'''



class FibonacciRpcClient(object):

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.queue_name = 'rpc_queue'
        # exclusive=True : 오직 현재 연결만 허용
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n)
        )
        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

for n in range(1, 1000):
    print(f' [x] Requesting fib({n})')
    response = fibonacci_rpc.call(n)
    print(f' [.] Got {response}\n')



        