import json
from rest_framework.authtoken.models import Token
from order.factories import UserFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from product.factories import CategoryFactory, ProductFactory


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        Token.objects.create(user=self.user)

        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(
            title='pro controller',
            price=200,
            categories=[self.category]
        )

    def test_product(self):
        token = Token.objects.get(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)['results'][0]

        self.assertEqual(product_data['title'], self.product.title)
        self.assertEqual(product_data['price'], self.product.price)
        self.assertEqual(product_data['active'], self.product.active)
        self.assertEqual(product_data['categories'][0]['title'], self.category.title)

    def test_create_product(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        category = CategoryFactory()

        payload = {
            'title': 'notebook',
            'price': 800.00,
            'categories_id': [category.id]
        }

        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product_data = json.loads(response.content)

        self.assertEqual(product_data['title'], payload['title'])
        self.assertEqual(product_data['price'], payload['price'])