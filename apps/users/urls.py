from django.urls import path
from .views import RegisterView

app_name = 'users'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='user-signup'),
]