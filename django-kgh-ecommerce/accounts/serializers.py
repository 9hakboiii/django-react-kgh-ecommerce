from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
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