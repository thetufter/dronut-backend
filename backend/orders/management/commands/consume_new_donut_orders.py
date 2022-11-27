from django.core.management.base import BaseCommand
import json
import time
from backend.consumer import Consumer
from orders.models import Order
from pika.exceptions import AMQPConnectionError


def try_to_create_order(channel, method, properties, body):
    payload = json.loads(body)
    Order.objects.create_order(**payload)


class Command(BaseCommand):
    help = 'Django command to consume new_donut_orders'

    def handle(self, *args, **options):
        while True:
            try:
                consumer = Consumer.get_consumer()
                consumer.consume(
                    routing_key='new_donut_order',
                    callback=try_to_create_order,
                )
            except AMQPConnectionError:
                print(' AMQP Connection Error. We will retry. To exit press CTRL+C')
                time.sleep(30)
