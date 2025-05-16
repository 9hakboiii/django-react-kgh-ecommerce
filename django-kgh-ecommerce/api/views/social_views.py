from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

#소셜 로그인 시점에 Allauth 내부에서 자동으로 호출
#사용자 생성, 로그인 전 처리 등을 커스터마이징할 수 있는 핵심 지점
# 전체 흐름 순서 요약
# 1. Provider callback → views.py
# 2. complete_social_login(request, sociallogin)
# 3. get_adapter(request) → DefaultSocialAccountAdapter
# 4. adapter.pre_social_login()
# 5. adapter.populate_user()
# 6. adapter.save_user()
# 7. login(request, user)

#dev_9_1_Fruit
class KakaoLoginView(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter