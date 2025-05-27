from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

# dev_5_fruit
# djsoer 회원가입 커스텀 마이징
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "gender",
            "job",
            # "old_cart",
        )

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "email",
            "gender",
            "job",
            "old_cart",
            "create_at",
            "update_at",
        )

# dev_9_2_fruit
# 로그인 했을 때, 커스텀 필드로 표시
class UserResAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "gender",
            "job",
            "old_cart",
            "created_at",
            "updated_at",
        )

#http://127.0.0.1:8000/api/dj-rest-auth/registration/
#https://dj-rest-auth.readthedocs.io/en/latest/configuration.html#register-serializer
class UserRegisterRestAuthSerializer(RegisterSerializer):
    #추가 필드 정의
    gender = serializers.ChoiceField(choices=User.GenderChoices.choices, required=True)
    job = serializers.ChoiceField(choices=User.JOBS, required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['gender'] = self.validated_data.get('gender','')
        data['job'] = self.validated_data.get('job','')

        return data

    def custom_signup(self, request, user):
        # 추가 필드 저장
        user.gender = self.validated_data.get('gender')
        user.job = self.validated_data.get('job')

        user.save()