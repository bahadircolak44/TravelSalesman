import json
import os
import pika


class PubSub:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST')
        self.port = os.getenv('RABBITMQ_PORT')
        self.routing_key = os.getenv('RABBITMQ_ROUTING_KEY')
        self.exchange_type = os.getenv('RABBITMQ_EXCHANGE_TYPE')
        self.consumer_exchange = os.getenv('CONSUMER_EXCHANGE', 'problems')
        self.producer_exchange = os.getenv('PRODUCER_EXCHANGE', 'solutions')
        self.receive_binding = True
        self.solution = None
        self.connection = self.establish_connection()
        self.channel = self.connection.channel()

    def establish_connection(self):
        connection_param = pika.ConnectionParameters(host=self.host)
        return pika.BlockingConnection(connection_param)

    def emit(self, problem):
        self.channel.exchange_declare(exchange=self.producer_exchange, exchange_type=self.exchange_type)
        self.channel.basic_publish(
            exchange=self.producer_exchange, routing_key=self.routing_key, body=problem)
        return self.receiver()

    def receiver(self):
        self.channel.exchange_declare(exchange=self.consumer_exchange, exchange_type=self.exchange_type)
        # let the server choose a random queue name for us.
        # set exclusive true for deleted the queue after consumer connection is closed.
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.consumer_exchange, queue=queue_name, routing_key='#')
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        # self.channel.start_consuming()
        while self.receive_binding:
            self.channel.connection.process_data_events(time_limit=int(os.getenv('TIME_LIMIT', 5)))  # 1 second
        return self.solution

    def callback(self, ch, method, properties, body):
        # Let's give some time for connection (Only for developing purposes)
        solution = json.loads(body.decode())
        self.solution = solution
        self.receive_binding = False
        return
