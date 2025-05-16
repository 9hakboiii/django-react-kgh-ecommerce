from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Category

from django.shortcuts import get_object_or_404
from rest_framework import status

# dev_32
from api.serializers.category_serializers import (
    CategorySerializer,
    CategorySimpleSerializer,
)

# dev_35
from rest_framework.views import APIView

# http://127.0.0.1:8000/api/categories/
# 방식   url         기능
# GET   categories/    list


# dev_32
@api_view(["GET"])
def categories_api(request):

    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# dev_35


class CategoriesAPI(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySimpleSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class CategoryAPI(APIView):

    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySimpleSerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySimpleSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response("삭제 성공", status=status.HTTP_204_NO_CONTENT)


# dev_36
# GenericAPIView: self.get_queryset()과 self.get_serializer()를 제공
# ListModelMixin: self.list() 내부에서 위의 메서드들을 호출
# 주의
# 기본적으로는 queryset, serializer_classs는 약속된 이름
# 대신 커스텀 마이징은 가능
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.generics import GenericAPIView


class CategoriesMixins(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# http://127.0.0.1:8000/api/category/2/
# http://127.0.0.1:8000/api/category/{name}/
# http://127.0.0.1:8000/api/category/자바/


class CategoryMixins(
    UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySimpleSerializer
    # lookup_field = "name"

    def get(self, request, *args, **kwargs):
        print("args:", args)
        print("kwargs:", kwargs)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# dev_37
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# generics.CreateAPIView : 생성
# generics.ListAPIView : 목록
# generics.RetrieveAPIView : 조회
# generics.DestroyAPIView : 삭제
# generics.UpdateAPIView : 수정
# generics.RetrieveUpdateAPIView : 조회/수정
# generics.RetrieveDestroyAPIView : 조회/삭제
# generics.ListCreateAPIView : 목록/생성
# generics.RetrieveUpdateDestroyAPIView : 조회/수정/삭제

# 권한
# AllowAny	누구나 접근 가능 (기본값)
# IsAuthenticated	로그인한 사용자만 접근 가능
# IsAdminUser	is_staff=True인 관리자만 접근 가능
# IsAuthenticatedOrReadOnly	읽기는 모두 허용, 쓰기는 인증 사용자만 가능
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


# 같은 이름의 카테고리가 이미 존재할 경우 오류
class CategoriesGenericView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]

    # create 함수를 오버라이딩
    def create(self, request, *args, **kwargs):
        name = request.data.get("name")

        # 같은 이름의 카테고리가 이미 존재할 경우 오류 메세지
        if Category.objects.filter(name=name).exists():
            raise ValidationError({"message": "같은 이름의 카테고리가 있습니다."})

        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "카테고리가 성공적으로 생성 되었습니다.",
            "category": response.data,
        }

        return response


# Get  category/{id}       category
# PUT  category/{id}       modify category
# DELETE  category/{id}    delete category


class CategoryGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySimpleSerializer

    # 조회시 로그 찍기
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"조회 카테고리 ID {instance.id} - {instance.name}")
        return super().retrieve(request, *args, **kwargs)

    # 수정 시 로깅 및 응답 커스텀 마이징
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        print(f"수정 카테고리 이름 {instance.name} -> {request.data.get("name")}")
        respose = super().update(request, *args, **kwargs)  # update 쿼리 날아감
        respose.data = {
            "message": f"수정 카테고리 이름 {instance.name} -> {request.data.get("name")}",
            "category": respose.data,
        }

        return respose

    # class DestroyModelMixin:
    #     """
    #     Destroy a model instance.
    #     """
    #     def destroy(self, request, *args, **kwargs):
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    #     def perform_destroy(self, instance):
    #         instance.delete()

    # HTTP DELETE 요청 →
    # → destroy() 실행 →
    # → perform_destroy(instance) 호출 →
    # → 객체 삭제

    # 카테고리 자바는 삭제 되지 않도록 처리
    from rest_framework.exceptions import ValidationError, PermissionDenied

    def perform_destroy(self, instance):

        if instance.name == "자바":
            raise ValidationError("이 카테고리는 관리자만이 삭제 가능 합니다.")

        print(f"[삭제] 카테고리 {instance.name} 삭제됨")
        instance.delete()

    # 삭제 응답 커스텀 마이징
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())

        return Response(
            {"message": "카테고리가 삭제 되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )


# dev_38
from rest_framework.viewsets import ModelViewSet

# ModelViewSet 또한 Mixins 집합이므로 아래를 기본적으로 상속 되어 제공되는 메소드가 있음
# create - POST /
# list - GET /
# retrieve - GET /
# update - PUT /
# partial_update - PATCH /
# destroy - DELETE /

from rest_framework.decorators import action
from rest_framework import filters

#dev_3_Fruit
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    #serializer_class = CategorySimpleSerializer
    #dev_10_Fruit
    serializer_class = CategorySerializer

