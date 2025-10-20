from rest_framework import generics,permissions,status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer,UserUpdateSerializer,UserReadSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"회원가입 성공"}, status=status.HTTP_201_CREATED)


class MyPageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserReadSerializer

    def get_object(self):
        if getattr(self, "swagger_fake_view", False):
            return User()

        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            raise NotAuthenticated(detail="인증필요")
        return user

    def get_serializer_class(self):
        if self.request.method in ("GET",):
            return UserReadSerializer
        return UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == 'PATCH'
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": " 업데이트 성공","data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self,request,*args,**kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message":"Deleted successfully"}, status=status.HTTP_200_OK)