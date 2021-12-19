import json
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
        pass

    def receive(self):
        pass

    def callback(self):
        pass