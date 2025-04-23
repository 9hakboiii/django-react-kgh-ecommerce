from django.shortcuts import render, redirect
from store.models import Product, Category

from django.contrib import messages


# dev_1
# dev_5
def home(request):
    products = Product.objects.all()  # 모든 상품을 가져옴
    return render(request, "store/home.html", {"products": products})


# dev_8
def about(request):
    return render(request, "store/about.html", {})


# dev_13
def product(request, product_id):
    product = Product.objects.get(id=product_id)  # 상품 ID로 상품을 가져옴
    return render(request, "store/product.html", {"product": product})


# dev_14
def category_summary(request):
    categories = Category.objects.all()  # 모든 카테고리를 가져옴
    return render(request, "store/category_summary.html", {"categories": categories})


# dev_14
def category(request, category_id):

    try:
        category = Category.objects.get(
            id=category_id
        )  # 카테고리 ID로 카테고리를 가져옴
        products = Product.objects.filter(
            category=category
        )  # 해당 카테고리의 상품을 가져옴 (1:N 관계, Product 모델의 category 필드)

        context = {"category": category, "products": products}
        return render(request, "store/category.html", context)
    except:
        messages.error(request, "존재하지 않는 카테고리입니다.")
        return redirect("store:home")
