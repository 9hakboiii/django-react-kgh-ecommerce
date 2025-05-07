
from rest_framework.views import APIView
# ✅ 카트 API endpoint 예시:
# HTTP       Method	       Endpoint	 기능
# GET	   /api/cart/	   장바구니       조회
# POST	   /api/cart/	   장바구니에    상품 추가
# PUT	   /api/cart/	   장바구니    상품 수량 변경
# DELETE   /api/cart/	   상품 제거 or 전체 비우기
# DELETE에서 product_id를 넘기면 해당 상품만 제거, 안 넘기면 전체 비움 처리됩니다.
from decimal import Decimal
from store.models import Product
from api.serializers.product_serializers import ProductSerializer
class CartAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self,request):
        """
        장바구니 목록 조회
        """
        # json 을 딕셔러니 객체로
        cart = json.loads(request.user.old_cart or "{}") 
        
        cart_items = []
        total_quantity = 0
        total_price = Decimal("0.00")

        for proudct_id, item in cart.items():
            try:
                product = Product.objects.get(id=proudct_id)
            except Product.DoesNotExist:
                continue # 없는 상품은 제외

            price = product.sale_price if product.is_sale else product.price

            quantity = item.get("quantity",0)
            item_total = Decimal(price) * quantity

            cart_items.append(
                {
                    "product": ProductSerializer(product).data,
                    "quantity": quantity,
                    "price": str(price),
                    "total_price": str(item_total),
                }
            )

            total_quantity += quantity
            total_price += item_total
        
        return Response(
            {
                "cart": cart_items,
                "cart_total_items": total_quantity,
                "cart_total_price": str(total_price),
            }
        )


    def post(self,request):
        pass
    
    def put(self,request):
        pass

    def delete(self,request):
        pass


import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#dev_6_Fruit
# POST	   /api/cart/merge	  장바구니에    상품 추가
class CartMergeAPIView(APIView):
    permission_classes = [IsAuthenticated] #로그인된 사람만 아래 함수가 실행 되도록

    def post(self,request):
        """
        localStorage의 장바구니를 서버 old_cart에 병합
        """
        user = request.user

        local_storage_cart = request.data.get("cart","{}")

        local_storage_cart = json.loads(local_storage_cart or "{}")
        old_cart = json.loads(user.old_cart or "{}")

        # 병합: 같은 상품이 있다면 수량 증가
        for product_id, item in local_storage_cart.items():
            quantity = int(item.get("quantity", 0))
            if product_id in old_cart:
                old_cart[product_id]["quantity"] += quantity
            else:
                old_cart[product_id] = {"quantity": quantity}

        user.old_cart = json.dumps(old_cart) #json을 string 만들어서 집어 넣어야함
        user.save()

        return Response({"message": "장바구니가 병합되었습니다."})