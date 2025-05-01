from django.urls import path, include
from .views import base_views, product_views, category_views

# dev_28
app_name = "api"


# dev_38
from rest_framework import routers

router = routers.DefaultRouter()
router.register("categories", category_views.CategoryViewSet)

category_list = category_views.CategoryViewSet.as_view(
    {"get": "list", "post": "create"}
)

category_detail = category_views.CategoryViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    # path("hello-world/", base_views.hello_world),
    # path("hello-world-json/", base_views.hello_world_json),
    # path("hello-world-drf/", base_views.hello_world_drf),
    # dev_29 proudct_view.py
    # http://127.0.0.1:8000/api/products/
    # 방식   url                 기능
    # GET  products/            list
    # POST products/            create
    # Get  product/{id}         product
    # PUT  product/{id}       modify product
    # DELETE  product/{id}    delete product
    path("products/", product_views.products_api),
    path("product/<int:pk>/", product_views.product_api),
    # dev_32
    # path("categories/", category_views.categories_api),
    # dev_35
    # 방식   url                  기능
    # GET  categories/           list
    # POST categories/           create
    # Get  category/{id}       category
    # PUT  category/{id}       modify category
    # DELETE  category/{id}    delete category
    # path("categories/", category_views.CategoriesAPI.as_view()),
    # path("category/<int:pk>/", category_views.CategoryAPI.as_view()),
    # dev_36
    # path("categories/", category_views.CategoriesMixins.as_view()),
    # path("category/<str:name>/", category_views.CategoryMixins.as_view()),
    # dev_37
    # path("categories/", category_views.CategoriesGenericView.as_view()),
    # path("category/<int:pk>/", category_views.CategoryGenericView.as_view()),
    # dev_38
    # 이렇게 하면 다음 경로들이 자동으로 만들어집니다
    # GET /categories/
    # POST /categories/
    # GET /categories/<pk>/
    # PUT /categories/<pk>/
    # PATCH /categories/<pk>/
    # DELETE /categories/<pk>/
    path("", include(router.urls)),
    # path("categories/", category_list),
    # path("category/<int:pk>", category_detail),

    # dev_5_fruit
    path("auth/", include("djoser.urls")), # 회원가입, 비밀번호 변경 등
    path("auth/", include("djoser.urls.jwt")) # JWT 로그인/로그아웃, 토큰 갱신 등
]
