from rest_framework.routers import DefaultRouter
from apps.accounts.views import AccountsViewSet

router = DefaultRouter()
router.register(r"accounts", AccountsViewSet, basename="accounts")

urlpatterns = router.urls