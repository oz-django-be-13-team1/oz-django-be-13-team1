from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer
from rest_framework.exceptions import PermissionDenied


# 로그인한 사용자의 모든 거래 내역을 조회
class TransactionHistoryListView(generics.ListAPIView,):
    serializer_class = TransactionHistorySerializer
    permission_classes = [AllowAny]

    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filterset_fields = ['transaction_direction', 'transaction_type', 'amount'] # 조건 2개 이상 필터링
    ordering_fields = ['transaction_at', 'amount']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return TransactionHistory.objects.none()

        user = getattr(self.request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return TransactionHistory.objects.none()

        return TransactionHistory.objects.filter(account__user_id=user.id)


# 로그인한 사용자의 거래 내역을 수정 및 삭제
class TransactionHistoryDetailView(generics.RetrieveUpdateDestroyAPIView) :
    serializer_class = TransactionHistorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return TransactionHistory.objects.none()

        user = getattr(self.request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return TransactionHistory.objects.none()

        return TransactionHistory.objects.filter(account__user_id=user.id)

    def perform_update(self, serializer):
        if self.get_object().account.user != self.request.user:
            raise PermissionDenied("본인의 거래만 수정할 수 있습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.get_object().account.user != self.request.user:
            raise PermissionDenied("본인의 거래만 삭제 할 수 있습니다.")
        instance.delete()



