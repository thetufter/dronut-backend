import pika
from django.conf import settings


class Consumer:
    def __init__(self, host, username, password, port=5672):
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username, password),
        )
        self.connection = None

    def consume(self, routing_key, callback):
        queue_name = routing_key
        if not self.connection:
            self._init_connection()
        self._init_channel()
        self._init_queue(queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
        )
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def _init_connection(self):
        self.connection = pika.BlockingConnection(self.parameters)

    def _init_channel(self):
        self.channel = self.connection.channel()

    def _init_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    @classmethod
    def get_consumer(cls):
        return cls(**settings.RABBITMQ_SETTINGS)
