from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from store.models import Product
from django.contrib import messages


# dev_15
def add_cart(request):
    cart = Cart(request)

    print("카트======", cart)

    # product.html에서 넘어온 데이터 (ajax)
    if request.POST.get("action") == "post":

        # 상품 받아오기
        product_id = int(request.POST.get("product_id"))
        print("product_id", product_id)

        # 상품 수량 받아오기
        product_qty = int(request.POST.get("product_qty"))
        print("product_qty", product_qty)

        # DB에서 상품 가져오기
        product = get_object_or_404(Product, id=product_id)

        # 세션에 저장
        cart.add(product, product_qty)

        # dev_16
        # 카트 전체 개수 가져오기
        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty})
        # cart.decrypt_all_sessions()  # dev_17

        # dev_22
        messages.success(
            request, "장바구니에 상품이 담겼습니다."
        )  # 장바구니에 상품 담기 성공 메시지

        # product.html에서 ajax로 응답하기 위해 JsonResponse 사용
        return response


# dev_18
def summary_cart(request):

    # 카트객체 받아 오기
    cart = Cart(request)

    return render(
        request,
        "cart/summary_cart.html",
        {"cart": cart, "totals": cart.get_product_total},  # dev_21
    )


# dev_19
def delete_cart(request):

    # 카트객체 받아 오기
    cart = Cart(request)

    # summary_cart.html에서 넘어온 데이터 (ajax)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))

        product = Product.objects.get(id=product_id)
        cart.remove(product)  # 장바구니에서 상품 삭제

        # dev_22
        messages.success(
            request, "장바구니에 삭제되었습니다"
        )  # 장바구니에 상품 삭제 성공 메시지

        return JsonResponse({"삭제 성공": product_id})


# dev_20
def update_cart(request):
    cart = Cart(request)

    # summary_cart.html에서 넘어온 데이터 (ajax)
    if request.POST.get("action") == "update":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        product = Product.objects.get(id=product_id)

        # 카트 업데이트(카트 추가가 아님)
        cart.add(product, product_qty, True)

        # dev_22
        messages.success(
            request, "장바구니에 해당 상품이 업데이트 되었습니다."
        )  # 장바구니에 상품 업데이트 성공 메시지

        return JsonResponse({"상품 업데이트": product_id})
