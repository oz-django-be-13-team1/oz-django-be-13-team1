from datetime import timedelta
from django.utils import timezone
from django.db import transaction as db_transaction
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import serializers

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .permissions import IsOwner

class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # 권한 설정: 본인만 접근 가능
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # 본인이 소유한 계좌만 조회 가능
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        pass

    def destroy(self, request, *args, **kwargs):
        # 계좌 삭제 시 잔액이 0인지 확인하는 로직
        instance = self.get_object()
        if instance.balance != 0.00:
            return Response(
                {"detail": "잔액이 남아있는 계좌는 삭제할 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)
        # 삭제 성공 시 204 상태 코드와 함께 사용자 정의 메시지를 반환
        return Response({"detail": "계좌가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

class TransactionViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # 계좌 소유자만 접근 가능
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # 본인 소유 계좌의 거래 내역만 필터링
        return Transaction.objects.filter(account__user=self.request.user).select_related('account')

    @db_transaction.atomic
    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']

        if account.user != self.request.user:
            raise permissions.PermissionDenied("본인의 계좌에 대해서만 거래를 생성할 수 있습니다.")

        new_balance = account.balance

        # 입금
        if serializer.validated_data['transaction_type'] == 'deposit':
            new_balance += amount
        # 출금
        elif serializer.validated_data['transaction_type'] == 'withdrawal':
            if account.balance < amount:
                raise serializers.ValidationError("잔액이 부족합니다.")
            new_balance -= amount

        account.balance = new_balance
        account.save(update_fields=['balance'])

        serializer.save(
            user=self.request.user,
            transaction_type=serializer.validated_data['transaction_type'],
            amount=amount,
            account=account
        )


COOKIE_ACCESS_NAME = "access"
COOKIE_REFRESH_NAME = "refresh"
COOKIE_COMMON = {
    "httponly": True,
    "samesite": "Lax",
    "secure": False,
    "path": "/",
}


def _set_tokens_to_response(resp, access, refresh):
    """응답에 Access/Refresh 토큰을 쿠키로 설정하는 헬퍼 함수"""
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
    """응답에서 쿠키 토큰을 제거하는 헬퍼 함수"""
    resp.delete_cookie(COOKIE_ACCESS_NAME, path="/")
    resp.delete_cookie(COOKIE_REFRESH_NAME, path="/")
    return resp


class CookieTokenObtainPairView(TokenObtainPairView):
    """쿠키 기반 JWT 토큰 발급 (로그인)"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access = response.data.get("access")
        refresh = response.data.get("refresh")
        resp = Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
        return _set_tokens_to_response(resp, access, refresh)


class CookieTokenRefreshView(TokenRefreshView):
    """쿠키 기반 JWT 토큰 재발급 (리프레시)"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            refresh_cookie = request.COOKIES.get(COOKIE_REFRESH_NAME)
            if not refresh_cookie:
                return Response({"detail": "refresh 토큰이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            request.data["refresh"] = refresh_cookie

        response = super().post(request, *args, **kwargs)
        new_access = response.data.get("access")
        new_refresh = response.data.get("refresh") or request.data.get("refresh")

        resp = Response({"message": "리프레시 성공"}, status=status.HTTP_200_OK)
        return _set_tokens_to_response(resp, new_access, new_refresh)


class CookieLogoutView(APIView):
    """쿠키 기반 JWT 로그아웃 (토큰 블랙리스트 처리 및 쿠키 제거)"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_cookie = request.COOKIES.get(COOKIE_REFRESH_NAME)
        if refresh_cookie:
            try:
                token = RefreshToken(refresh_cookie)
                # 토큰을 블랙리스트에 추가하여 재사용 불가능하게 처리
                token.blacklist()
            except Exception:
                pass

        resp = Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        return _clear_tokens(resp)


class HeaderLogoutView(APIView):
    """헤더 기반 JWT 로그아웃 (토큰 블랙리스트 처리)"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh = request.data.get("refresh") or request.query_params.get("refresh")
        if not refresh:
            return Response({"detail": "refresh 토큰이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh)
            # 토큰을 블랙리스트에 추가하여 재사용 불가능하게 처리
            token.blacklist()
        except Exception:
            # 토큰이 유효하지 않아도 200 응답
            pass

        return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)


class MeView(APIView):
    """현재 로그인된 사용자 정보 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response(
            {
                "user_id": str(u.user_id),
                "email": u.email,
                "nickname": u.nickname,
            },
            status=status.HTTP_200_OK,
        )
