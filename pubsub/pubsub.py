import json
import time

import pika


class PubSub:
    def __init__(self):
        self.host = 'localhost'
        self.port = '5672'

        self.connection = self.establish_connection()
        self.channel = self.connection.channel()

    def establish_connection(self):
        connection_param = pika.ConnectionParameters(host=self.host)
        return pika.BlockingConnection(connection_param)

    def publish(self, solution):
        self.channel.exchange_declare(exchange='solutions', exchange_type='topic')
        self.channel.basic_publish(
            exchange='solutions', routing_key='travel.salesman', body=solution)

    def receive(self):
        self.channel.exchange_declare(exchange='problems', exchange_type='topic')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='problems', queue=queue_name, routing_key='#')
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        # Let's give some time for connection (Only for developing purposes)
        time.sleep(0.3)
        data = json.loads(body.decode())
        print(f'Received Problem: {data}')
