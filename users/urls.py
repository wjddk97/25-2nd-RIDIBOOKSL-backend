from django.urls import path

from users.views import KakaoLoginView

urlpatterns = [
    path('/sign-in/kakao', KakaoLoginView.as_view())
]