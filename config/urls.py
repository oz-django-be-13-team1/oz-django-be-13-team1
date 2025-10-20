
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.shortcuts import redirect
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="MY API",
        default_version='v1',
        description="API 문서입니다",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # 로그인 없이 접근
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/transactions/", include("apps.transaction_history.urls")),
    path("api/auth/", include(("apps.accounts.urls", "accounts"), namespace="accounts")), # accounts/urls/__init__.py에서 auth_urls 포함

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('', lambda request: redirect('schema-swagger-ui')),


]
