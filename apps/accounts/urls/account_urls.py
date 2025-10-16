from rest_framework.routers import DefaultRouter
from apps.accounts.views import AccountViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"transactions", TransactionViewSet, basename="transactions")

urlpatterns = router.urls