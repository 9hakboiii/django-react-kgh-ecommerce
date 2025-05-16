from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, Category

# dev_34
from api.serializers.product_serializers import ProductSerializer

# http://127.0.0.1:8000/api/products/
# 방식   url         기능
# GET   products/    list
# POST  products/   create


#http://127.0.0.1:8000/api/products/?ordering=-price

# dev_29
@api_view(["GET", "POST"])
def products_api(request):

    if request.method == "GET":
        products = Product.objects.all()
        # many=True ➜ 여러 개의 인스턴스 (QuerySet, 리스트 등)
        # many=False (기본값) ➜ 단일 인스턴스
        serializer = ProductSerializer(products, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    # dev_30
    # 디시리얼라이져
    # if request.method == "POST":
    #     print("데이터", request.data)  # json , dic
    #     print("타입", type(request.data))  # json , dic

    #     serializer = ProductSerializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data)

    # dev_33 view 에서 직접 처리
    if request.method == "POST":

        # request.data 는 기본적으로 불변임
        data = request.data.copy()

        # category 정보 추출 후 제거
        category_data = data.pop("category")
        category_data = request.data["category"]

        # get_or_create 는 dict 형식으로 받기 때문에 category_data는 리스트일 수 있어서 주의
        if isinstance(category_data, list):
            category_data = category_data[0]

        # 카테고리 저장 조회
        category, _ = Category.objects.get_or_create(**category_data)

        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)

        return Response(serializer.data)


from django.shortcuts import get_object_or_404
from rest_framework import status


# dev_30
@api_view(["GET", "DELETE", "PUT"])
def product_api(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "GET":
        # many=True ➜ 여러 개의 인스턴스 (QuerySet, 리스트 등)
        # many=False (기본값) ➜ 단일 인스턴스
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        product.delete()
        return Response("SUCCESS", status=status.HTTP_204_NO_CONTENT)

#dev_10_Fruit
# 페이지네이션 클래스 (옵션)

# GET /api/product-list/
# 요청 예시
# /api/product-list/?page=2	페이지 2
# /api/product-list/?search=포도	'포도' 포함 검색
# /api/product-list/?category=4	카테고리 ID가 4번인 상품 필터링
# /api/product-list/?ordering=price	가격 오름차순 정렬
# /api/product-list/?ordering=-id	최신순 정렬
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

#http://127.0.0.1:8000/api/product-list/?page_size=5
#http://127.0.0.1:8000/api/product-list/?/api/products/?page=3&page_size=25

#LimitOffsetPagination
#CursorPagination
# {
    # "count": 21,
    # "next": "http://127.0.0.1:8000/api/product-list/?page=2&page_size=5",
    # "previous": null,
    # "results": [
    #     {

class ProductPagination(PageNumberPagination):
    page_size = 10 # 기본 페이지 크기
    page_size_query_param = "page_size"  # 클라이언트가 지정할 수 있는 파라미터
    max_page_size = 100  # 최대 페이지 크기 제한

# 장고에서 쿼리스트링 필터 만들기
import django_filters
# GET /api/product-list/?category=1&min_price=1000&max_price=3000

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte') # >=
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte') # <=

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']   


# ModelViewSet
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    #  추가
    filterset_class = ProductFilter
    # 필터링 항목 (URL에서 ?category=값 으로 필터링 가능)
    filterset_fields = ['category']


    # 정렬/검색 
    #http://127.0.0.1:8000/api/products/?ordering=-price
    # 요청을 가로채서 필터셋(filterset_class)을 확인.
    # 정의된 필드와 비교해 유효한 필터만 추출
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
        
    # 정렬 필드 (?ordering=price )
    #http://127.0.0.1:8000/api/product-list/?ordering=-price
    ordering_fields = ['id','price','name']
    ordering = ['id']

    # 검색 필드 (?search=아이폰)
    #Product.objects.filter(name__icontains='컴퓨터')
    search_fields = ['name','description'] # 필요에 따라 수정 가능