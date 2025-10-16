from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path("auth/", include("apps.accounts.urls.auth_urls")),
    path("account/", include("apps.accounts.urls.account_urls")),
]