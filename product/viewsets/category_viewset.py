from rest_framework.viewset import  ModelViewset

from product.models import  Category

from product.serializers.category_serializer import CategorySerializer

class CategoryViewset(ModelViewset):
    serializer_class = CategorySerializer
 
def get_queryset(self):
 return Category.objects.all().order_by('id')