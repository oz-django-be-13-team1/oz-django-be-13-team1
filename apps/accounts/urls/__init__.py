from django.urls import path, include

urlpatterns = [
    path("", include("apps.accounts.urls.auth_urls")),
]
