from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


# dev_10
# 1. 모델 2. 검증 3. html 코드 작성해줌
class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "job",
            "gender",
        ]

    # dev_11
    # bootstrap을 사용하기 위해서 init 메소드 오버라이딩
    # 1. 모든 필드에 Bootstrap form-control 클래스 추가
    def init(self, args, **kwargs):
        super().init(args, **kwargs)

        # 모든 필드에 Bootstrap form-control 클래스 추가
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

        # 성별 선택을 위한 Bootstrap form-select 클래스 추가
        self.fields["gender"].widget.attrs.update({"class": "form-select"})

        # 직업 선택을 위한 Bootstrap form-select 클래스 추가
        self.fields["job"].widget.attrs.update({"class": "form-select"})
