from rest_framework.views import APIView

# ✅ 카트 API endpoint 예시:
# HTTP       Method           Endpoint     기능
# GET       /api/cart/       장바구니       조회
# POST       /api/cart/       장바구니에    상품 추가
# PUT       /api/cart/       장바구니    상품 수량 변경
# DELETE   /api/cart/       상품 제거 or 전체 비우기
# 🔁 DELETE에서 product_id를 넘기면 해당 상품만 제거, 안 넘기면 전체 비움 처리됩니다.

class CartAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        # 장바구니 조회 로직
        pass

    def post(self, request):
        # 장바구니에 상품 추가 로직
        pass

    def put(self, request):
        # 장바구니 상품 수량 변경 로직
        pass

    def delete(self, requset):
        # 장바구니 상품 제거 or 전체 비우기 로직
        pass