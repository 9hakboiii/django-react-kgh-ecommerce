from .cart import Cart


# dev_17
def cart(request):
    # 세션확인 테스트
    # cart.decrypt_all_sessions()
    print("카트 함수 호출")
    return {"cart": Cart(request)}  # 장바구니 객체를 템플릿 컨텍스트에 추가하여 사용
