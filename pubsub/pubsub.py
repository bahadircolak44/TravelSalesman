import json
import os
import time

import pika

from ortool import main


class PubSub:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST')
        self.port = os.getenv('RABBITMQ_PORT')
        self.routing_key = os.getenv('RABBITMQ_ROUTING_KEY')
        self.exchange_type = os.getenv('RABBITMQ_EXCHANGE_TYPE')
        self.consumer_exchange = os.getenv('CONSUMER_EXCHANGE', 'problems')
        self.producer_exchange = os.getenv('PRODUCER_EXCHANGE', 'solutions')
        self.connection = self.establish_connection()
        self.channel = self.connection.channel()

    def establish_connection(self):
        connection_param = pika.ConnectionParameters(host=self.host)
        return pika.BlockingConnection(connection_param)

    def publish(self, solution):
        self.channel.exchange_declare(exchange=self.producer_exchange, exchange_type=self.exchange_type)
        self.channel.basic_publish(
            exchange=self.producer_exchange, routing_key=self.routing_key, body=solution)

    def receive(self):
        self.channel.exchange_declare(exchange=self.consumer_exchange, exchange_type=self.exchange_type)
        # let the server choose a random queue name for us.
        # set exclusive true for deleted the queue after consumer connection is closed.
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.consumer_exchange, queue=queue_name, routing_key='#')
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        # Let's give some time for connection (Only for developing purposes)
        time.sleep(0.5)
        data = json.loads(body.decode())
        print(f'Received Problem: {data}')

        problem = dict(locations=data, num_vehicles=1, depot=0)
        solution = main(problem)
        self.publish(json.dumps(solution).encode())


if __name__ == '__main__':
    ps = PubSub()
    ps.receive()
