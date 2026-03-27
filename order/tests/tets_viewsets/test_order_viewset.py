import json
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        Token.objects.create(user=self.user)

        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(
            title='mouse',
            price=100,
            categories=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)['results'][0]

        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)
        self.assertEqual(
            order_data['product'][0]['category']['title'],
            self.category.title
        )

    def test_create_order(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        product = ProductFactory()

        payload = {
            'product_id': [product.id],
            'user': self.user.id,
        }

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_data = json.loads(response.content)

        self.assertEqual(order_data['user'], self.user.id)
        self.assertEqual(len(order_data['product']), 1)
        self.assertEqual(order_data['product'][0], product.id)