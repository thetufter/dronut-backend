from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from donuts.models import Donut
from orders.models import Order, CREATED


class CreateOrderCase(TestCase):
    def setUp(self):
        self.donut1 = Donut.objects.create(
            donut_code='test1',
            name='Test 1',
            price_per_unit=2.00
        )
        self.donut2 = Donut.objects.create(
            donut_code='test2',
            name='Test 2',
            price_per_unit=2.50
        )

    def test_create_order(self):
        '''Create an order with a standard correct input should success with:
            - correct customer_line
            - correct order total price
            - CREATED status
            - correct donut for each line
            - correct quantity for each line
            - correct price for each line 
        '''
        order = Order.objects.create_order(
            customer_name='John Smith',
            donuts=[
                {'donut_code': 'test1', 'quantity': 2},
                {'donut_code': 'test2', 'quantity': 2},
            ]
        )
        self.assertEqual(order.customer_name, 'John Smith')
        self.assertEqual(order.price, 9)
        self.assertEqual(order.status, CREATED)
        line1 = order.lines.all()[0]
        self.assertEqual(line1.donut, self.donut1)
        self.assertEqual(line1.quantity, 2)
        self.assertEqual(line1.price, 4.00)
        line2 = order.lines.all()[1]
        self.assertEqual(line2.donut, self.donut2)
        self.assertEqual(line2.quantity, 2)
        self.assertEqual(line2.price, 5.00)

    def test_create_order_with_non_string_customer_name(self):
        '''Create an order with non-string customer_name should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid customer_name"):
            Order.objects.create_order(
                customer_name=123,
                donuts=[
                    {'donut_code': 'test1', 'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_empty_string_customer_name(self):
        '''Create an order with empty string customer_name should fail'''
        with self.assertRaisesMessage(ValidationError, "Empty customer_name is not allowed"):
            Order.objects.create_order(
                customer_name='   ',
                donuts=[
                    {'donut_code': 'test1', 'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_non_list_donuts(self):
        '''Create an order with non-list donuts should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid donuts"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts={'donut_code': 'test1', 'quantity': 2},
            )

    def test_create_order_with_empty_list_donuts(self):
        '''Create an order with empty list donuts should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid donuts"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[]
            )

    def test_create_order_with_non_dict_donut(self):
        '''Create an order with non-dict donut should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid donut: test1"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    'test1',
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_no_donut_code(self):
        '''Create an order with no donut_code should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid donut: {'quantity': 2}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_non_string_donut_code(self):
        '''Create an order with no donut_code should fail'''
        with self.assertRaisesMessage(ValidationError, "donut_code must be a string: {'donut_code': 123, 'quantity': 2}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': 123, 'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_empty_string_donut_code(self):
        '''Create an order with empty string donut_code should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid donut_code: {'donut_code': '  ', 'quantity': 2}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': '  ', 'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_non_slug_donut_code(self):
        '''Create an order with non-slug donut_code should fail'''
        with self.assertRaisesMessage(ValidationError, "Invalid donut_code: {'donut_code': '  test1', 'quantity': 2}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': '  test1', 'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_donut_has_no_quantity(self):
        '''Create an order with a donut with no quantity should success
            and assume quantity=1
        '''
        order = Order.objects.create_order(
            customer_name='John Smith',
            donuts=[
                {'donut_code': 'test1'},
                {'donut_code': 'test2', 'quantity': 2},
            ]
        )
        self.assertEqual(order.customer_name, 'John Smith')
        self.assertEqual(order.price, 7)
        self.assertEqual(order.status, CREATED)
        line1 = order.lines.all()[0]
        self.assertEqual(line1.donut, self.donut1)
        self.assertEqual(line1.quantity, 1)
        self.assertEqual(line1.price, 2.00)
        line2 = order.lines.all()[1]
        self.assertEqual(line2.donut, self.donut2)
        self.assertEqual(line2.quantity, 2)
        self.assertEqual(line2.price, 5.00)

    def test_create_order_with_non_integer_quantity(self):
        '''Create an order with non-integer quantity should fail'''
        with self.assertRaisesMessage(ValidationError, "quantity must be a positive integer: {'donut_code': 'test1', 'quantity': 't'}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': 'test1', 'quantity': 't'},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_zero_quantity(self):
        '''Create an order with zero quantity should fail'''
        with self.assertRaisesMessage(ValidationError, "quantity must be a positive integer: {'donut_code': 'test1', 'quantity': 0}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': 'test1', 'quantity': 0},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_negative_integer_quantity(self):
        '''Create an order with negative integer quantity should fail'''
        with self.assertRaisesMessage(ValidationError, "quantity must be a positive integer: {'donut_code': 'test1', 'quantity': -2}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': 'test1', 'quantity': -2},
                    {'donut_code': 'test2', 'quantity': 2},
                ]
            )

    def test_create_order_with_repeated_donut_code(self):
        '''Create an order with repeated donut code should success
            and accumulate the quantity
        '''
        order = Order.objects.create_order(
            customer_name='John Smith',
            donuts=[
                {'donut_code': 'test1'},
                {'donut_code': 'test2', 'quantity': 2},
                {'donut_code': 'test1', 'quantity': 2},
            ]
        )
        self.assertEqual(order.customer_name, 'John Smith')
        self.assertEqual(order.price, 11)
        self.assertEqual(order.status, CREATED)
        line1 = order.lines.all()[0]
        self.assertEqual(line1.donut, self.donut1)
        self.assertEqual(line1.quantity, 3)
        self.assertEqual(line1.price, 6.00)
        line2 = order.lines.all()[1]
        self.assertEqual(line2.donut, self.donut2)
        self.assertEqual(line2.quantity, 2)
        self.assertEqual(line2.price, 5.00)

    def test_create_order_with_a_nonexistent_donut_code(self):
        '''Create an order with a nonexistent donut code should fail'''
        with self.assertRaisesMessage(ObjectDoesNotExist, "No donut(s) with the following code(s): {'test3'}"):
            Order.objects.create_order(
                customer_name='John Smith',
                donuts=[
                    {'donut_code': 'test1', 'quantity': 2},
                    {'donut_code': 'test2', 'quantity': 2},
                    {'donut_code': 'test3', 'quantity': 2},
                ]
            )
