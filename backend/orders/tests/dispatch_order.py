from django.test import TestCase
from django.core.exceptions import BadRequest
from donuts.models import Donut
from orders.models import Order, DISPATCHED


class DispatchOrderCase(TestCase):
    def setUp(self):
        Donut.objects.create(
            donut_code='test1',
            name='Test 1',
            price_per_unit=2.00
        )
        Donut.objects.create(
            donut_code='test2',
            name='Test 2',
            price_per_unit=2.50
        )

    def test_dispatch_a_created_order(self):
        '''Dispatch a CREATED order should success'''
        order = Order.objects.create_order(
            customer_name='John Smith',
            donuts=[
                {'donut_code': 'test1', 'quantity': 2},
                {'donut_code': 'test2', 'quantity': 2},
            ]
        )
        order.dispatch()
        self.assertEqual(order.status, DISPATCHED)

    def test_dispatch_a_dispatched_order(self):
        '''Dispatch a DISPATCHED order should fail'''
        order = Order.objects.create_order(
            customer_name='John Smith',
            donuts=[
                {'donut_code': 'test1', 'quantity': 2},
                {'donut_code': 'test2', 'quantity': 2},
            ]
        )
        order.dispatch()

        with self.assertRaisesMessage(BadRequest, f'Order #{order.id} was already dispatched'):
            order.dispatch()
