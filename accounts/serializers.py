from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email","password","bio","profile_image","birth_date","created_at","updated_at")
        read_only_fields = ["created_at", "updated_at"]


    def create(self,validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is Required")
        return value
    def validate_password(self, value):
        validate_password(value)
        return value
    
class LoginSerialzer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise AuthenticationFailed("Incorrect Email or Password")
            if not user.is_active:
                raise AuthenticationFailed("This account has been disabled")
            
        else:
            return serializers.ValidationError("You Must Enter You Email, and Password")
        
        data["user"] = user
        return data
    

class ProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email","bio","profile_image","birth_date","created_at", "updated_at")
        read_only_fields = ("email","created_at", "updated_at")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self,val):
        user = self.context["request"].user

        if not user.check_password(val):
            raise serializers.ValidationError("Incorrect Old Password")

        return val
    
    def validate_new_password(self,val):
        if len(val) < 8:
            raise serializers.ValidationError("Invalid Password")
        
        return val
    
    def save(self, *args, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        return user

        
