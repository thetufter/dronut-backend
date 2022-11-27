from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.producer import Producer
from donuts.models import Donut
from donuts.serializers import DonutSerializer


@receiver(post_save, sender=Donut)
def produce_message(sender, instance, created, **kwargs):
    try:
        action = 'donut_created' if created else 'donut_updated'
        producer = Producer.get_producer()
        producer.produce(
            body={
                'action': action,
                'donut': DonutSerializer(instance).data,
            },
            routing_key='donuts'
        )
    except:
        print('Producing a message failed')
