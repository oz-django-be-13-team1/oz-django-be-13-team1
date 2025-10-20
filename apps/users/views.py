from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer,UserUpdateSerializer,UserReadSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"회원가입 성공"}, status=status.HTTP_201_CREATED)


class MyPageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("GET",):
            return UserReadSerializer
        return UserUpdateSerializer

    def destory(self,request,*args,**kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message":"Deleted successfully"}, status=status.HTTP_200_OK)