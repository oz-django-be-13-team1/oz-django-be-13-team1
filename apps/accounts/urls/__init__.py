from django.urls import path, include
from .auth_urls import urlpatterns as auth_urls
from .account_urls import urlpatterns as account_urls

app_name = "accounts" # 네임 스페이스 명시
urlpatterns = [
    path("", include(auth_urls)),
    path("", include(account_urls)),
]
