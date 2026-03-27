from django.test import TestCase

from product.serializers.product_serializer import ProductSerializer
from product.factories import CategoryFactory


class ProductSerializerTest(TestCase):

    def test_serializer_valid(self):
        category = CategoryFactory()

        data = {
            "title": "Produto Teste",
            "price": 50,
            "categories_id": [category.id],
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_without_title(self):
        category = CategoryFactory()

        data = {
            "price": 50,
            "categories_id": [category.id],
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
