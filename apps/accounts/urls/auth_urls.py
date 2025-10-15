from django.urls import path
from apps.accounts.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieLogoutView,
    HeaderLogoutView,
    MeView
)

app_name = "accounts"
urlpatterns = [
    path("cookie/login/",   CookieTokenObtainPairView.as_view(), name="cookie-login"),
    path("cookie/refresh/", CookieTokenRefreshView.as_view(), name="cookie-refresh"),
    path("cookie/logout/",  CookieLogoutView.as_view(), name="cookie-logout"),
    path("jwt/logut/", HeaderLogoutView.as_view(), name="jwt-logut"),
]
