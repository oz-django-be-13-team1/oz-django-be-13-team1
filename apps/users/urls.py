from django.urls import path
from .views import RegisterView, MyPageView

app_name = 'users'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='user-signup'),
    path("me/", MyPageView.as_view(), name='me'),
]