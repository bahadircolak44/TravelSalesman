import json
import os
import pika


class PubSub:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = os.getenv('RABBITMQ_PORT', '5672')
        self.routing_key = os.getenv('RABBITMQ_ROUTING_KEY', 'travel.salesman')
        self.exchange_type = os.getenv('RABBITMQ_EXCHANGE_TYPE', 'topic')
        self.consumer_exchange = os.getenv('CONSUMER_EXCHANGE', 'problems')
        self.producer_exchange = os.getenv('PRODUCER_EXCHANGE', 'solutions')
        self.receive_binding = True
        self.solution = None
        self.connection = self.establish_connection()
        self.channel = self.connection.channel()

    def establish_connection(self):
        """
        Create rabbitmq connection with host and port parameters
        :return: connection
        """
        connection_param = pika.ConnectionParameters(host=self.host)
        return pika.BlockingConnection(connection_param)

    def emit(self, problem):
        """
        allowing the customer to input problem instances
        :param problem: JSON object with max_travel_distance, num_vehicles, depot and locations
        :return: the solution received from underlying pub/sub queue
        """
        self.channel.exchange_declare(exchange=self.producer_exchange, exchange_type=self.exchange_type)
        self.channel.basic_publish(
            exchange=self.producer_exchange, routing_key=self.routing_key, body=problem)
        return self.receiver()

    def receiver(self):
        """
        !! THIS FUNCTION IS JUST FOR DEBUG !!

        Configure rabbitmq with required params to listen queue
        :return:
        """
        self.channel.exchange_declare(exchange=self.consumer_exchange, exchange_type=self.exchange_type)
        # let the server choose a random queue name for us.
        # set exclusive true for deleted the queue after consumer connection is closed.
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.consumer_exchange, queue=queue_name, routing_key='#')
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        # start_consuming will call process_data_events in infinite loop, which doesn't require for this
        # when solution received, loop need to
        while self.receive_binding:
            self.channel.connection.process_data_events(time_limit=int(os.getenv('TIME_LIMIT', 5)))

        self.receive_binding = True
        return self.solution

    def callback(self, ch, method, properties, body):
        """
        The callback function. Calls when results received from the underlying pub/sub queues.
        """
        # Let's give some time for connection (Only for developing purposes)
        solution = json.loads(body.decode())
        self.solution = solution
        self.receive_binding = False
        return
