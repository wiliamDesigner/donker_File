from django.urls import path, include
from rest_framework import routers
from order import views

router = routers.SimpleRouter()
router.register(r'order', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]