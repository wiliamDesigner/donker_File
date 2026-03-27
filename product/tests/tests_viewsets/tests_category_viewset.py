import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='books')

    def test_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_data = json.loads(response.content)['results'][0]

        self.assertEqual(category_data['title'], self.category.title)

    def test_create_category(self):
        payload = {
            'title': 'tecnologia',
        }

        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title='tecnologia')

        self.assertEqual(created_category.title, 'tecnologia')

   