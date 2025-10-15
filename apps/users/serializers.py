from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=15)

    class Meta:
        model = User
        fields = ["email","password","nickname","name","phone_number"]

    def create(self,validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id","email","nickname","name","phone_number","last_login"]
        read_only_fields = ["user_id","email","last_login"]

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False,allow_blank=True)

    class Meta:
        model = User
        fields = ['email','password','nickname','name','phone_number']
        read_only_fields = ['user_id','email','last_login']

    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance