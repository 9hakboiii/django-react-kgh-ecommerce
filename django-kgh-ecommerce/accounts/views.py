from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.forms import RegisterUserForm
from accounts.models import User
import json

from cart.cart import Cart
from store.models import Product

"""
class HTTPRequest:
    POST = {
        "username": "admin",
        "password": "1234",
    }
"""


# dev_9
def login_user(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        # login.html input 태그의 name 속성값과 일치해야 함
        username = request.POST["username"]
        password = request.POST["password"]

        # DB에 저장된 사용자 정보와 비교하여 인증
        # authenticate() 메서드의 리턴값이 None이 아니면 인증 성공
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # dev_23
            current_user = User.objects.get(id=request.user.id)
            saved_cart = current_user.old_cart

            # add
            cart = Cart(request)
            if len(cart) > 0:  # cart/cart.py의 __len__() 메서드 사용
                cart.cart_to_db()

            if saved_cart:
                # string을 json으로 변환
                # items()를 사용해서 for문 돌릴려고 json 사용하는것
                converted_cart = json.loads(saved_cart)

                # {"1": {"quantity": 5, "price": "10000"}}
                # loop
                for product_id, data in converted_cart.items():
                    quantity = data["quantity"]
                    print("상품 ID:", product_id)  # 1
                    print("수량:", quantity)  # 5
                    product = Product.objects.get(id=product_id)
                    cart.add(product, quantity)

            messages.success(request, "로그인 성공")
            return redirect("/")
        else:
            messages.error(request, "로그인에 실패하였습니다. 다시 입력해주세요.")
            return redirect("accounts:login_user")
            # return redirect("accounts: login_user") : namespace를 사용하여 URL을 지정할 수 있음

    return render(request, "accounts/login.html", {})


# dev_9
def logout_user(request):
    logout(request)  # session을 삭제하여 로그아웃 처리
    return redirect("/")


# dev_10
# dev_11 회원가입 로직
def register_user(request):

    form = RegisterUserForm()

    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            form = RegisterUserForm(request.POST)  # 폼에 POST 데이터 전달

            if form.is_valid():  # 폼 검증
                form.save()  # 회원 DB에 저장

                # 회원가입 하자 마자, 로그인 시켜줌 (검증 끝난 데이터)
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")

                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("/")
    else:
        form = RegisterUserForm()

    return render(request, "accounts/register.html", {"form": form})


# dev_27
def kakao_login_user(request):
    return render(request, "accounts/kakao_login.html")
