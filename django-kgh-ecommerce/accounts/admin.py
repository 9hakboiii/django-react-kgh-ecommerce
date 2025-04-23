from django.contrib import admin
from accounts.models import User

# Register your models here.
# dev_9

# dev_12
# 어드민 페이지 등록방법 3가지
# 1. 기본적인 관리자 페이지에서 기본적인 등록
# 하지만 커스텀 기능(검색, 필터, 필드 설정 등)을 추가할 수 없음
# admin.site.register(User)


# 2. ModelAdmin 클래스를 상속받아 커스터마이징 (검색, 필터, 필드 설정 등)
# class UserAccountsAdmin(admin.ModelAdmin):
#     list_display = [
#         "username",
#         "email",
#         "job",
#         "gender",
#     ]

#     # DB의 저장된 값을 기준으로 필터링
#     search_fields = [
#         "username",
#         "email",
#         "job",
#         "gender",
#     ]

#     # filter는 잘 사용 안 함
#     list_filter = [
#         "username",
#         "email",
#         "job",
#         "gender",
#     ]

# admin.site.register(User, UserAccountsAdmin)


# 3. @admin.register 데코레이터를 사용하여 커스터마이징
@admin.register(User)
class UserAccountsAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "job",
        "gender",
    ]

    search_fields = [
        "username",
        "email",
        "job",
        "gender",
    ]

    list_filter = [
        "username",
        "job",
        "gender",
    ]
