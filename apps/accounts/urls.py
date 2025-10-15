from django.urls import path
from .views import CookieTokenObtainPairView, CookieTokenRefreshView, CookieLogoutView

app_name = "accounts"
urlpatterns = [
    path("cookie/login/",   CookieTokenObtainPairView.as_view(), name="cookie-login"),
    path("cookie/refresh/", CookieTokenRefreshView.as_view(),    name="cookie-refresh"),
    path("cookie/logout/",  CookieLogoutView.as_view(),          name="cookie-logout"),
]
