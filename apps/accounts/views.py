from datetime import timedelta

from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

COOKIE_ACCESS_NAME = "access"
COOKIE_REFRESH_NAME = "refresh"
COOKIE_COMMON = {
    "httponly": True,
    "samesite": "Lax",
    "secure": False,
    "path": "/",
}

def _set_tokens_to_response(resp, access, refresh):
    if access:
        resp.set_cookie(
            COOKIE_ACCESS_NAME, str(access),
            expires=timezone.now() + timedelta(minutes=30),
            **COOKIE_COMMON
        )
    if refresh:
        resp.set_cookie(
            COOKIE_REFRESH_NAME, str(refresh),
            expires=timezone.now() + timedelta(days=3),
            **COOKIE_COMMON
        )
    return resp

def _clear_tokens(resp):
    resp.delete_cookie(COOKIE_ACCESS_NAME, path="/")
    resp.delete_cookie(COOKIE_REFRESH_NAME, path="/")
    return resp


class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access = response.data.get("access")
        refresh = response.data.get("refresh")
        resp = Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
        return _set_tokens_to_response(resp, access, refresh)


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            refresh_cookie = request.COOKIES.get(COOKIE_REFRESH_NAME)
            if not refresh_cookie:
                return Response({"detail": "refresh 토큰이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            request.data["refresh"] = refresh_cookie

        response = super().post(request, *args, **kwargs)
        new_access = response.data.get("access")
        new_refresh = response.data.get("refresh")

        if not new_refresh:
            new_refresh = request.data.get("refresh")

        resp = Response({"message": "리프레시 성공"}, status=status.HTTP_200_OK)
        return _set_tokens_to_response(resp, new_access, new_refresh)


class CookieLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_cookie = request.COOKIES.get(COOKIE_REFRESH_NAME)
        if refresh_cookie:
            try:
                token = RefreshToken(refresh_cookie)
                try:
                    token.blacklist()
                except Exception:
                    pass
            except Exception:
                pass

        resp = Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        return _clear_tokens(resp)

class HeaderLogoutView(APIView):
    permission_classes =  [permissions.AllowAny]

    def post(self,request):
        refresh = request.data.get("refresh") or request.query_params.get("refresh")
        if not refresh:
            return Response({"detail": "refresh 올바른 토믄을 부탁드립니다."}, status=400)
        try:
            token = RefreshToken(refresh)
            try:
                token.blacklist()
            except Exception:
                pass
        except Exception:
            pass

        return Response({"message": "로그아웃 왼료"},status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response(
            {
                "user_id": str(u.user_id),
                "email": u.email,
                "nickname": u.nickname,
                "name": u.name,
            },
            status=status.HTTP_200_OK,
        )
