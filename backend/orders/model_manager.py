from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from donuts.models import Donut
from backend.producer import Producer


class OrderManager(models.Manager):
    def create_order(self, customer_name, donuts):
        '''
        A method to create an order
        - customer_name: str
        - donuts: list of dictionaries:
            [ {'donut_code': 'abc', 'quantity': 2}, ]
        '''

        if not isinstance(customer_name, str):
            raise ValidationError('Invalid customer_name')

        if len(customer_name := customer_name.strip()) == 0:
            raise ValidationError('Empty customer_name is not allowed')

        if not isinstance(donuts, list) or len(donuts) < 1:
            raise ValidationError('Invalid donuts')

        data = {
            # donut_code: quantity,
        }

        for donut in donuts:
            if not isinstance(donut, dict) or 'donut_code' not in donut:
                raise ValidationError(f'Invalid donut: {donut}')

            donut_code = donut['donut_code']

            if not isinstance(donut_code, str):
                raise ValidationError(
                    f"donut_code must be a string: {donut}"
                )

            try:
                validate_slug(donut_code)
            except:
                raise ValidationError(f'Invalid donut_code: {donut}')

            quantity = donut['quantity'] if 'quantity' in donut else 1

            if not isinstance(quantity, int) or quantity < 1:
                raise ValidationError(
                    f"quantity must be a positive integer: {donut}"
                )

            if donut_code in data:
                data[donut_code] += quantity
            else:
                data[donut_code] = quantity

        donut_codes = set(data.keys())

        instances = Donut.objects.get_donuts_by_code(donut_codes)

        order = self.create(customer_name=customer_name)

        for instance in instances.all():
            quantity = data[instance.donut_code]
            order.lines.create(donut=instance, quantity=quantity)

        try:
            producer = Producer.get_producer()
            producer.produce(
                body={
                    'action': 'order_created',
                    'order_id': order.id,
                    'customer_name': order.customer_name,
                    'price': str(order.price),
                    'donuts': donuts,
                },
                routing_key='orders'
            )
        except:
            print('Producing a message failed')

        return order
