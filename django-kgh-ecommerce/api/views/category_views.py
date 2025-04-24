from store.models import Category
from api.serializers.category_serializers import CategorySimpleSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
