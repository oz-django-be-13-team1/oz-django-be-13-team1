# your_app/auth_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 2. 중복되던 JWT View import를 하나로 정리
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieLogoutView,
    HeaderLogoutView,
    MeView,
    AccountViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

app_name = "accounts"

urlpatterns = [
    path("cookie/login/",   CookieTokenObtainPairView.as_view(), name="cookie-login"),
    path("cookie/refresh/", CookieTokenRefreshView.as_view(), name="cookie-refresh"),
    path("cookie/logout/",  CookieLogoutView.as_view(), name="cookie-logout"),

    path("jwt/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("jwt/logout/", HeaderLogoutView.as_view(), name="jwt-logout"),

    # User info
    path("me/", MeView.as_view(), name="me"),
    path('', include(router.urls)),
]