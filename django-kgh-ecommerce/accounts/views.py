from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# from .forms import RegisterUserForm # 상대 경로형식
from accounts.forms import RegisterUserForm  # 절대 경로 형식

# dev_23
from accounts.models import User
import json
from cart.cart import Cart
from store.models import Product

# Create your views here.


# class HTTPRequest:
#    POST = {"username":"admim","password":"1234"}
#    GET = {}
# dev_9


def logout_user(request):
    logout(request)  # session 에 저장된 sessionid 삭제
    return redirect("/")


def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # session key 생성및 세션키 DB 저장

            # dev_23
            current_user = User.objects.get(id=request.user.id)
            saved_cart = (
                current_user.old_cart
            )  # {"3": {"quantity": 1, "price": "24000"}}
            # add
            #
            cart = Cart(request)

            if len(cart) > 0:
                cart.cart_to_db()

            if saved_cart:
                converted_cart = json.loads(saved_cart)  # string 을 Json 객체로

                # {"1": {"quantity": 5, "price": "10000"}}
                # loop
                for product_id, data in converted_cart.items():
                    quantity = data["quantity"]
                    print("상품 ID:", product_id)  # 1
                    print("수량:", quantity)  # 5
                    product = Product.objects.get(id=product_id)
                    cart.add(product, quantity)

            messages.success(request, "You Have been logged in")
            return redirect("/")
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect("accounts:login_user")
    else:
        return render(request, "accounts/login.html", {})


# dev_10
# dev_11 회원가입 로직
def register_user(request):

    if request.method == "POST":

        if request.POST["password1"] == request.POST["password2"]:
            form = RegisterUserForm(request.POST)  # 모델에 다가 값을 넣음

            if form.is_valid():
                form.save()  # 회원 DB 저장

                # 회원가입 하자 마자, 로그인 시켜줌
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
