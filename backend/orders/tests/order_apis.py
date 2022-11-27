import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from donuts.models import Donut
from orders.models import Order, DISPATCHED


class OrderAPIsCase(APITestCase):
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
        Order.objects.create_order(
            # id=1,
            customer_name='John Smith',
            donuts=[
                {'donut_code': 'test1', 'quantity': 2},
                {'donut_code': 'test2', 'quantity': 2},
            ]
        )
        Order.objects.create_order(
            # id=2,
            customer_name='Mark Smith',
            donuts=[
                {'donut_code': 'test1', 'quantity': 1},
                {'donut_code': 'test2', 'quantity': 3},
            ]
        )
        self.donuts_data = [
            {
                'donut_code': 'test1',
                'name': 'Test 1',
                'price_per_unit': '2.00'
            },
            {
                'donut_code': 'test2',
                'name': 'Test 2',
                'price_per_unit': '2.50'
            },
        ]
        self.orders_data = [
            {
                'id': 1,
                'customer_name': 'John Smith',
                'status': 'Created',
                'price': 9.0,
                'lines': [
                    {'donut': self.donuts_data[0],
                        'quantity': 2, 'price': 4.0},
                    {'donut': self.donuts_data[1],
                        'quantity': 2, 'price': 5.0},
                ]
            },
            {
                'id': 2,
                'customer_name': 'Mark Smith',
                'status': 'Created',
                'price': 9.5,
                'lines': [
                    {'donut': self.donuts_data[0],
                        'quantity': 1, 'price': 2.0},
                    {'donut': self.donuts_data[1],
                        'quantity': 3, 'price': 7.5},
                ]
            },
            {
                'id': 3,
                'customer_name': 'Max Smith',
                'status': 'Created',
                'price': 6.5,
                'lines': [
                    {'donut': self.donuts_data[0],
                        'quantity': 2, 'price': 4.0},
                    {'donut': self.donuts_data[1],
                        'quantity': 1, 'price': 2.5},
                ]
            },
        ]

    def test_list_orders_api(self):
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.orders_data[:2])

    def test_get_an_order_by_id_api(self):
        url = reverse('order-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.orders_data[0])

    def test_create_order_api(self):
        orders_count_before = Order.objects.count()
        url = reverse('order-list')
        data = {
            'customer_name': 'Max Smith',
            'donuts': [
                {'donut_code': 'test1', 'quantity': 2},
                {'donut_code': 'test2', 'quantity': 1},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), self.orders_data[2])
        orders_count_after = Order.objects.count()
        self.assertEqual(orders_count_after, orders_count_before + 1)

    def test_dispatch_an_order_by_id_api(self):
        url = reverse('order-detail', args=[2])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {'detail': 'Order #2 has been dispatched'}
        )
        order2 = Order.objects.get(id=2)
        self.assertEqual(order2.status, DISPATCHED)
