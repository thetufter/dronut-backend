from django.db import models
from django.core.exceptions import BadRequest
from django.core.validators import MinValueValidator
from orders.model_manager import OrderManager
from backend.producer import Producer

CREATED = 0
DISPATCHED = 1


class Order(models.Model):
    customer_name = models.CharField(max_length=1024)

    ORDER_STATUS_CHOICES = [
        (CREATED, 'Created'),
        (DISPATCHED, 'Dispatched'),
    ]

    status = models.IntegerField(
        choices=ORDER_STATUS_CHOICES,
        default=CREATED,
    )

    objects = OrderManager()

    def dispatch(self):
        if self.status == CREATED:
            self.status = DISPATCHED
            self.save()

            try:
                producer = Producer.get_producer()
                producer.produce(
                    body={
                        'action': 'order_dispatched',
                        'order_id': self.id,
                        'customer_name': self.customer_name,
                        'price': str(self.price),
                    },
                    routing_key='orders'
                )
            except:
                print('Producing a message failed')

        else:
            raise BadRequest(f'{self} was already dispatched')

    def get_price(self):
        return sum([l.price for l in self.lines.all()])

    @property
    def price(self):
        return self.get_price()

    def __str__(self):
        return f'Order #{self.id}'


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='lines',
    )

    donut = models.ForeignKey(
        'donuts.Donut',
        on_delete=models.CASCADE,
        related_name='order_lines',
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    def get_price(self):
        return self.quantity * self.donut.price_per_unit

    @property
    def price(self):
        return self.get_price()

    def __str__(self):
        return f'A line of order #{self.id}: {self.quantity} x {self.donut}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'donut'],
                name='order_and_donut_are_unique',
            )
        ]
