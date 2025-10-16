from django.urls import path
from .views import TransactionHistoryListView, TransactionHistoryDetailView

app_name = "transaction_history"

urlpatterns = [
    path('', TransactionHistoryListView.as_view(), name='transacion_history_list'), # 거래 내역 전체 목록 조회
    path('<int:pk>/', TransactionHistoryDetailView.as_view(), name='transacion_history_detail'), # 거래 내역 조회/수정/삭제
]
