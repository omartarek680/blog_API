from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerialzer, ProfileSerializer, ChangePasswordSerializer, RequestResetSerializer, ConfirmResetSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
# Create your views here.
@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user) 
        return Response({
            "message": "User has been successfully created",
            "id": user.id,
            "email": user.email,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def login(request):
    serializer = LoginSerialzer(data= request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    return Response({
            "message" : "login success",
            "email" : user.email,
            "token" : token.key
        })

@api_view(["POST"])
def logout(request):
    permission_classes = [IsAuthenticated]
    request.user.auth_token.delete()
    return Response(
            {"message": "Successfully logged out."}, 
            status=status.HTTP_200_OK
        )

    
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password Changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RequestResetPassword(APIView):

    def post(self,request):
        serializer = RequestResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:3000/reset/{uid}/{token}/"
        print(reset_link)

        return Response({"message": "Reset link sent"})

class ConfirmResetView(APIView):

    def post(self, request, uidb64, token):
        serializer = ConfirmResetSerializer(data=request.data)

        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(id=uid)
            except:
                return Response({"error": "Invalid UID"})

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid token"})

            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response({"message": "Password reset successful"})

        return Response(serializer.errors)
    def post(self,request):
        serializer = ConfirmResetSerializer(data=request.data)

        if serializer.is_valid():
            try:
                uidb64 = serializer.validated_data['uidb64']
                token = serializer.validated_data['token']
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(id=uid)
            except:
                return Response({"error": "Invalid UID"})           
            
            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid token"})
            
            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response({"message": "Password reset successful"})

        return Response(serializer.errors)