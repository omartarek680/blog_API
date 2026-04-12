from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerialzer, ProfileSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
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
    