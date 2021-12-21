import json
import os
import pika

from ortool import main
from logger import app_logger


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
        """
        Create rabbitmq connection with host and port parameters
        :return: connection
        """
        connection_param = pika.ConnectionParameters(host=self.host)
        return pika.BlockingConnection(connection_param)

    def publish(self, solution):
        """
        Publish the solution via solution pubsub queue
        :param solution: solution of the problem solved by ortools.
        :return: None
        """
        try:
            self.channel.exchange_declare(exchange=self.producer_exchange, exchange_type=self.exchange_type)
            self.channel.basic_publish(
                exchange=self.producer_exchange, routing_key=self.routing_key, body=solution)
        except Exception as ex:
            app_logger.error(f'Publisher Error: {str(ex)}')

    def receive(self):
        """
        Configure rabbitmq with required params to listen queue
        :return:
        """
        try:
            self.channel.exchange_declare(exchange=self.consumer_exchange, exchange_type=self.exchange_type)
            # let the server choose a random queue name for us.
            # set exclusive true for deleted the queue after consumer connection is closed.
            result = self.channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=self.consumer_exchange, queue=queue_name, routing_key='#')
            self.channel.basic_consume(
                queue=queue_name, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
        except Exception as ex:
            app_logger.error(f'Receiver Error: {str(ex)}')

    def callback(self, ch, method, properties, body):
        """
        Received problem JSON object with max_travel_distance, num_vehicles, depot and locations from customer.
        The solution will published from underlying pub/sub queue after ortool solve it.
        :return:
        """
        try:
            problem = json.loads(body.decode())
            app_logger.info(f'Problem Received: {problem}')
            solution = main(**problem)
            app_logger.info(f'Problem Solved: {solution}')
            self.publish(json.dumps(solution).encode())
        except Exception as ex:
            app_logger.error(f'Callback Error: {str(ex)}')


if __name__ == '__main__':
    ps = PubSub()
    ps.receive()
