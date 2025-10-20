from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.shortcuts import redirect

schema_view = get_schema_view(
    openapi.Info(
        title="MY API",
        default_version='v1',
        description="문서 설명 입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="example@gmail.com"),
        license=openapi.License(name="BSD License"),
    )
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/transactions/", include("apps.transaction_history.urls")),
    path("api/auth/", include(("apps.accounts.urls", "accounts"), namespace="accounts")), # accounts/urls/__init__.py에서 auth_urls 포함
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', lambda request: redirect('schema-swagger-ui')),


]

