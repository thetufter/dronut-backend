import pika
import json
from django.conf import settings


class Producer:
    def __init__(self, host, username, password, port=5672):
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username, password),
        )

    def produce(self, body, routing_key):
        queue = routing_key
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        connection.close()

    @classmethod
    def get_producer(cls):
        return cls(**settings.RABBITMQ_SETTINGS)
