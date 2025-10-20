from django.urls import path
from apps.accounts.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieTokenLogoutView,
    JWTLoginView,
    JWTRefreshView,
    JWTVerifyView,
    JWTLogoutView,
    UserSignupView,
)

urlpatterns = [
    # Cookie JWT
    path('cookie/login/', CookieTokenObtainPairView.as_view(), name='auth_cookie_login_create'),
    path('cookie/logout/', CookieTokenLogoutView.as_view(), name='auth_cookie_logout_create'),
    path('cookie/refresh/', CookieTokenRefreshView.as_view(), name='auth_cookie_refresh_create'),

    # 일반 JWT
    path('jwt/login/', JWTLoginView.as_view(), name='auth_jwt_login_create'),
    path('jwt/logout/', JWTLogoutView.as_view(), name='auth_jwt_logout_create'),
    path('jwt/refresh/', JWTRefreshView.as_view(), name='auth_jwt_refresh_create'),
    path('jwt/verify/', JWTVerifyView.as_view(), name='auth_jwt_verify_create'),

    # 회원가입
    path('../../users/signup/', UserSignupView.as_view(), name='users_signup_create'),
]