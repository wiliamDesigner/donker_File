from django.urls import path, include
from rest_framework import routers

from product import views

router = routers.SimpleRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'category', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]