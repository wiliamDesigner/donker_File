from django.test import TestCase
from django.contrib.auth import get_user_model
from order.serializers.order_serializer import OrderSerializer
from product.factories import ProductFactory


User = get_user_model()


class OrderSerializerTest(TestCase):

    def test_serializer_valid(self):
        user = User.objects.create_user(username="teste", password="123")

        product = ProductFactory()

        data = {
            "user": user.id,
            "products_id": [product.id]
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid())