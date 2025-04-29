from django.db import models


# dev_3
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    max_digits: (소수점 포함) 숫자 전체 자릿수
    decimal_places: 소수점 아래 자릿수 정의
    """

    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    # dev_30 => Json 처리를 위하여 blank, null 속성 추가
    image = models.ImageField(
        upload_to="upload/product", blank=True, null=True
    )  # 이미지의 URL을 저장 (db에 모든 이미지 저장 x)
    # dev_32 역방향 참조를 위한 related_name 설정
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )  # DB에선 카테고리 ID로 저장
    # dev_6
    is_sale = models.BooleanField(default=False)  # 할인 여부
    sale_price = models.IntegerField(default=0, blank=True, null=True)  # 할인 가격

    def __str__(self):
        return self.name
