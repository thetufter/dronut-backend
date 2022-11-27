import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from donuts.models import Donut


class DonutAPIsCase(APITestCase):
    def setUp(self):
        self.donuts_data = [
            {
                'id': '50ca2a91-49c6-46b1-85db-a9d1d883c3bf',
                'donut_code': 'abc_test1',
                'name': 'Test 1',
                'description': 'Test Donut 1',
                'price_per_unit': '2.00',
            },
            {
                'id': '9cbd8b44-fcbd-4ecd-9461-9387d714c941',
                'donut_code': 'abc_test2',
                'name': 'Test 2',
                'description': 'Test Donut 2',
                'price_per_unit': '2.50',
            },
            {
                'id': '246ec872-e445-4348-af85-60e7ae74ce2a',
                'donut_code': 'xyz_test3',
                'name': 'Test 3',
                'description': 'Test Donut 3',
                'price_per_unit': '3.00',
            },
        ]
        Donut.objects.create(**self.donuts_data[0])
        Donut.objects.create(**self.donuts_data[1])
        Donut.objects.create(**self.donuts_data[2])

    def test_list_donuts_api(self):
        url = reverse('donut-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.donuts_data)

    def test_list__and_filter_donuts_api(self):
        url = reverse('donut-list')
        response = self.client.get(f'{url}?q=abc', format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.donuts_data[:2])

    def test_get_a_donut_by_id_api(self):
        donut1_id = self.donuts_data[0]['id']
        url = reverse('donut-detail', args=[donut1_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.donuts_data[0])

    def test_create_donut_api(self):
        donuts_count_before = Donut.objects.count()
        url = reverse('donut-list')
        data = {
            'donut_code': 'xyz_test4',
            'name': 'Test 4',
            'description': 'Test Donut 4',
            'price_per_unit': '3.50'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        donuts_count_after = Donut.objects.count()
        self.assertEqual(donuts_count_after, donuts_count_before + 1)

    def test_update_a_donut_api(self):
        donut2_id = self.donuts_data[1]['id']
        url = reverse('donut-detail', args=[donut2_id])
        request_data = {
            'name': 'Test 2 UPDATED',
            'description': 'Test Donut 2 UPDATED',
            'price_per_unit': '4.50',
        }
        response = self.client.patch(url, request_data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_data = {
            'id': donut2_id,
            'donut_code': 'abc_test2',
            'name': 'Test 2 UPDATED',
            'description': 'Test Donut 2 UPDATED',
            'price_per_unit': '4.50',
        }
        self.assertEqual(json.loads(response.content), response_data)
