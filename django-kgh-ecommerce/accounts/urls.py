from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

# dev_9
app_name = "accounts"

# 이름 짓는법 = 변수, 함수 , 클래스 이름
# login_user
# login_user
# 의미_그룹(통일)

urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.register_user, name="register_user"), #dev_10
    # dev_27
    path("kakao_login_user/", views.kakao_login_user, name="kakao_login_user"), 
]
