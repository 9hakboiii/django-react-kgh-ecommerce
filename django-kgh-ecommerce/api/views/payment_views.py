from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Category

from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework import viewsets
from payment.models import Payment
from api.serializers.payment_serializers import PaymentSerializer, ShippingAddressSerializer



#dev_8_2_Fruit
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


    # create 커스텀 마이징
    # POST /api/payments/ – 결제 내역 생성 커스텀 마이징
    def create(self,request,*args, **kwargs):
        # 1. 주문 생성
        # 2. 배송지 저장 (user, order를 함께 저장)
        # 3. 결제 저장 (serializer 사용 가능)

        try:
            user = request.user
            imp_uid = request.data.get("imp_uid")
            paid_amount = request.data.get("paid_amount")
            shippingData = request.data.get("shippingData")

            print("서버 결재 처리===", user,imp_uid, paid_amount,shippingData)
            
            from orders.models import Order, OrderItem
            
            #1.주문 생성
            order = Order.objects.create(
                user=user,
                amount_paid=paid_amount,
            )

            print("1.주문 생성완료", order)

            #2.배송지 저장
            shipping_serializer = ShippingAddressSerializer(data=shippingData)
            shipping_serializer.is_valid(raise_exception=True)
            shipping = shipping_serializer.save(user=user,order=order)

            print("2. 배송지 저장 완료",shipping) 

            # 3. 결제 저장 (serializer 사용 가능)
            payment_serializer = self.get_serializer(
                data = {
                    "imp_uid": imp_uid,
                    "user": user.id,
                    "order": order.id,
                    "paid_amount": paid_amount,
                }
            )
            payment_serializer.is_valid(raise_exception=True)
            payment = payment_serializer.save()

            print("3. 결제 저장 완료", payment)

            # 4. 응답 반환
            return Response(
                {
                    "message":"결제 및 주문 저장 성공",
                    "order_id": order.id,
                    "payment_id": payment.id,
                },
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            print(e)
            return Response(
                {
                    "error" : str(e),
                    "detail": "❌ 결제 처리 중 오류가 발생했습니다.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )    




