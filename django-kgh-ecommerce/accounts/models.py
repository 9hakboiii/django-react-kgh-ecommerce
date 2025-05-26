from django.db import models
from django.contrib.auth.models import AbstractUser


# dev_9
# User 계정을 커스터 마이징 시키는 방법은 4가지 정도가 있다.
# 1. proxy 확용 2. AbstractUser 상속 3. AbstractBaseUser 상속 4. UserManager 상속
class User(AbstractUser):

    # TestChoices는 Django에서 제공하는 TextChoices의 상속받은 클래스이다.
    # admin 페이지에서는 남자, 여자로 보인다.
    class GenderChoices(models.TextChoices):
        MALE = "M", "남자"
        FEMAIL = "F", "여자"

    # max_length는 DB에서의 길이 제한을 의미한다. (M, F)
    # verbose_name은 admin 페이지에서 보여지는 이름을 의미한다.
    # choices는 선택지를 의미한다.
    gender = models.CharField(
        verbose_name="성별", max_length=1, choices=GenderChoices.choices
    )

    # 튜플로 만들면 P, S, R, E는 DB에 저장되는 값이고
    # 교수/강사, 학생, 연구원, 기타는 admin 페이지에서 보여지는 값이다.
    JOBS = (
        ("P", "교수/강사(Professor/Lecturer)"),
        ("S", "학생(Student)"),
        ("R", "연구원(Researcher)"),
        ("E", "기타(Etc.)"),
    )

    job = models.CharField(verbose_name="직업", max_length=1, choices=JOBS)

    # 생성과 수정 시각을 자동으로 저장하는 필드이다.
    # auto_now_add는 객체가 처음 생성될 때의 시각을 저장한다.
    # auto_now는 객체가 수정될 때의 시각을 저장한다.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # dev_23
    # 장바구니 정보를 db에 저장 (session에 저장하는 것과는 다름)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    # dev_9_1_Fruit
    profile_image = models.URLField(blank=True, null=True)