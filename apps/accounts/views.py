from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

# 회원가입 + 조회 (GET/POST)

class UserSignupView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "username and password required"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created", "username": user.username}, status=201)

    def get(self, request):
        # 모든 사용자 조회용 (Swagger에서 GET 테스트 가능)
        users = User.objects.all().values("id", "username")
        return Response({"users": list(users)}, status=200)


# JWT 쿠키 방식
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "access" in response.data:
            response.set_cookie("access", response.data["access"], httponly=True)
        if "refresh" in response.data:
            response.set_cookie("refresh", response.data["refresh"], httponly=True)
        return response

    def get(self, request, *args, **kwargs):
        return Response({"info": "POST로 로그인 후 쿠키 발급"}, status=200)


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
        if "access" in response.data:
            response.set_cookie("access", response.data["access"], httponly=True)
        return response

    def get(self, request):
        return Response({"info": "POST로 쿠키 리프레시"}, status=200)


class CookieTokenLogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

    def get(self, request):
        return Response({"info": "POST로 로그아웃"}, status=200)


# 일반 JWT 방식
class JWTLoginView(TokenObtainPairView):
    def get(self, request):
        return Response({"info": "POST로 로그인, 토큰 발급"}, status=200)


class JWTRefreshView(TokenRefreshView):
    def get(self, request):
        return Response({"info": "POST로 토큰 리프레시"}, status=200)


class JWTVerifyView(TokenVerifyView):
    def get(self, request):
        return Response({"info": "POST로 토큰 검증"}, status=200)


class JWTLogoutView(APIView):
    def post(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        return Response({"info": "POST로 로그아웃"}, status=200)
