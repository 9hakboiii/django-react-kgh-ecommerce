from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from store.models import Product
from decimal import Decimal
from accounts.models import User
import json
from decimal import Decimal



# dev_15
class Cart:  # 카트 클래스 생성

    def __init__(self, request):  # 객체 생성시 request 객체를 받도록 함
        self.session = request.session  # 세션 객체를 클래스 내에서 사용하기 위해 저장

        # dev_23
        self.request = request  # request 객체를 클래스 내에서 사용하기 위해 저장

        cart = self.session.get(
            settings.CART_SESSION_ID
        )  # 세션에서 CART_SESSION_ID에 해당하는 장바구니 정보 가져오기

        if not cart:  # 장바구니 정보가 세션에 없을 경우
            # 새로운 빈 장바구니 객체를 세션에 할당
            # save()가 실행되기 전까지 db에 세션에 저장되지 않음
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart  # 클래스의 cart 속성에 세션 내 장바구니 정보 저장

    # dev_16
    def __len__(self):
        return sum(
            item["quantity"] for item in self.cart.values()
        )  # 장바구니에 담긴 상품의 총 수량을 반환

    # dev_21(장바구니의 모든 상품 가격)
    def get_product_total(self):
        return sum(
            item["quantity"] * Decimal(item["price"]) for item in self.cart.values()
        )

    # dev_18
    def __iter__(self):
        product_ids = self.cart.keys()  # 장바구니에 담긴 상품 ID 목록 {"1", "2", ...}

        products = Product.objects.filter(
            id__in=product_ids
        )  # DB에서 상품 ID에 해당하는 상품 객체를 가져옴

        """
        cart = {
            "1": {"quantity": 1, "price": "10000.00", "product": <Product: 상품1},
            ...
        }
        """

        for product in products:  # 상품 객체를 순회하며
            # 장바구니에 상품 객체를 추가
            self.cart[str(product.id)]["product"] = product

        """
        cart = {
            "1": {"quantity": 1, "price": "10000.00", "product": <Product: 상품1, "total_price": <item["price"] * item["quantity"]>},
            ...
        }
        """
        for item in self.cart.values():  # 장바구니의 각 상품에 대해
            # 가격을 Decimal로 변환 (문자열을 Decimal로 변환)
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]  # 총 가격 계산

            yield item  # 제너레이터 문법

    def add(self, product, quantity=1, is_update=False):
        """
        장바구니에 상품을 추가하거나 업데이트하는 메서드

        :param product: 추가할 상품 객체 (상품의 id와 price를 사용)
        :param quantity: 추가할 상품의 수량 (기본값은 1)
        :param is_update: 수량을 업데이트할지 여부를 나타내는 플래그 (기본값은 False)
        """
        product_id = str(
            product.id
        )  # 상품 객체의 ID를 문자열로 변환하여 사용 (세션에서 key로 사용)

        """
        cart = {
            "1": {"quantity": 1, "price": "10000"},
            ...
        }
        """

        if product_id not in self.cart:  # 장바구니에 해당 상품 ID가 없는 경우 새로 추가

            # dev_21
            if product.is_sale:
                self.cart[product_id] = {
                    "quantity": 0,
                    "price": str(product.sale_price),
                }
            else:
                self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if is_update:
            self.cart[product_id][
                "quantity"
            ] = quantity  # is_update 플래그가 True인 경우 수량을 해당 값으로 설정
        else:
            self.cart[product_id][
                "quantity"
            ] += quantity  # is_update가 False인 경우 현재 수량에 추가 수량을 더함

        self.save()  # 장바구니 정보 저장

    # dev_23
    def cart_to_db(self):
        # 로그인이 되어 있는 유저라면
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id)
            # convert {'3': 1} to {"3": 1 } (JSON 형식으로 변환, JSON은 작은따옴표를 허용하지 않음)
            carty = str(self.cart)
            carty = carty.replace("'", '"')  # 문자열의 작은따옴표를 큰따옴표로 변경
            current_user.update(old_cart=str(carty))  # 장바구니 정보를 DB에 저장

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart  # 세션에 장바구니 정보 저장
        self.session.modified = (
            True  # 세션이 수정되었음을 표시하여 Django가 세션을 저장하도록 함
        )
        # dev_23
        self.cart_to_db()

    # dev_19
    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # dev_24
    def get_cart(self):
        """장바구니 정보를 딕셔너리 형태로 반환"""
        return self.cart

    # dev_16
    def decrypt_all_sessions(self):
        """현재 DB에 저장된 모든 세션을 복호화하여 출력"""
        sessions = Session.objects.all()  # DB에서 모든 세션 조회

        if not sessions.exists():
            print("❌ 현재 저장된 세션이 없습니다.")
            return

        print(f"🔹 총 {sessions.count()}개의 세션을 찾았습니다.")

        for session in sessions:
            try:
                session_data = SessionStore(
                    session_key=session.session_key
                ).load()  # 세션 복호화
                print(f"✅ 세션 키: {session.session_key}\n   데이터: {session_data}\n")

            except Exception as e:
                print(f"❌ 복호화 실패 - 세션 키: {session.session_key}, 오류: {e}")


#dev_7_Fruit
 # ✅ old_cart 데이터 
 # {
 # "34": {"quantity": 1, "price": "10000.00"}, 
 # "33": {"quantity": 1, "price": "12000.00"}
 # }
class CartDRF:

    def __init__(self,reqeust):
        self.request = reqeust

    #상품 전제 삭제 메서드
    def remove_from_old_cart(self,user,proudct_id):
        old_cart = user.old_cart or "{}"
        cart = json.loads(old_cart)

        proudct_id = str(proudct_id)

        if proudct_id in cart:
            del cart[proudct_id]
            user.old_cart = json.dumps(cart)
            user.save()

        
    # 상품 추가 메서드
    def add_to_old_cart(self, user, product_id, price, quantity):
        
        # 기존 cart 불러오기 (없으면 빈 dict)
        old_cart = user.old_cart or "{}"
        cart = json.loads(old_cart)

        product_id = str(product_id)
        price = str(price)

        # 이미 상품이 있으면 수량 증가
        if product_id in cart:
            cart[product_id]["quantity"] += quantity
        else: # 카트안에 상품 번호가 없으면 새로 생성
            cart[product_id] = {
                "quantity": quantity,
                "price": price,
            } 

        # 다시 json 형태로 변환
        user.old_cart = json.dumps(cart)
        user.save()
