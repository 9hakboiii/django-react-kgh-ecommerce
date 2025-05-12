from django.urls import path, include
from .views import base_views, product_views, category_views, cart_views


# dev_28
app_name = "api"
from .views import base_views, product_views, category_views, cart_views, social_views


# dev_38
from rest_framework import routers

router = routers.DefaultRouter()
router.register("categories", category_views.CategoryViewSet)

# dev_8_fruit
# GET /api/payments/ – 전체 결제 내역
# POST /api/payments/ – 결제 내역 생성
# GET /api/payments/<id>/ – 단일 결제 조회
# PUT/PATCH /api/payments/<id>/ – 수정
# DELETE /api/payments/<id>/ – 삭제
from api.views.payment_views import PaymentViewSet
router.register("payments", PaymentViewSet)

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
    path("auth/", include("djoser.urls.jwt")), # JWT 로그인/로그아웃, 토큰 갱신 등
    # dev_6_fruit
    path("cart/", cart_views.CartAPIView.as_view()),
    path("cart/merge/", cart_views.CartMergeAPIView.as_view()),
    # dev_9_1_fruit
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("dj-rest-auth/kakao/", social_views.KakaoLoginView.as_view(), name="kakao_login"),
]

# ✅ 기본 엔드포인트 목록 (JWT 기준)
# HTTP Method    Endpoint URL    설명
# POST    /dj-rest-auth/login/    로그인 (JWT 또는 세션)
# POST    /dj-rest-auth/logout/    로그아웃 (세션 삭제 or 쿠키 삭제)
# POST    /dj-rest-auth/registration/    회원가입
# POST    /dj-rest-auth/password/change/    비밀번호 변경
# POST    /dj-rest-auth/password/reset/    비밀번호 초기화 이메일 전송
# POST    /dj-rest-auth/password/reset/confirm/    비밀번호 초기화 완료
# GET    /dj-rest-auth/user/    현재 로그인된 사용자 정보 가져오기
# PUT/PATCH    /dj-rest-auth/user/    사용자 정보 수정
# ✅ JWT 사용 시 추가 엔드포인트
# (dj-rest-auth 설정에서 USE_JWT = True 설정한 경우)
# HTTP Method    Endpoint URL    설명
# POST    /dj-rest-auth/token/refresh/    access token 재발급
# POST    /dj-rest-auth/token/verify/    JWT 유효성 검증
# ✅ 소셜 로그인 시 추가 엔드포인트 (예: Kakao, Google 등)
# allauth 및 dj-rest-auth.registration을 함께 설정해야 합니다.
# HTTP Method    Endpoint URL    설명
# POST    /dj-rest-auth/social/login/    소셜 로그인 (provider, access_token 전달)
# POST    /dj-rest-auth/registration/    소셜 로그인 시 회원가입