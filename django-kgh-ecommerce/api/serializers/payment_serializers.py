from rest_framework import serializers
from store.models import Category, Product

from payment.models import Payment
from orders.models import ShippingAddress

#dev_8_2_Fruit
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__" #주문 포함


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = ["user","order"]