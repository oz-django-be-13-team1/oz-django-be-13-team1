from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Accounts
from .serializers import  AccountsSerializer

# ModelViewSet을 상속받아 CRUD 기능을 한 번에 구현하고자 함
class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Accounts.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # 삭제 성공 시 204 상태 코드와 함께 사용자 정의 메시지를 반환시킴
        return Response({"detail": "계좌가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
