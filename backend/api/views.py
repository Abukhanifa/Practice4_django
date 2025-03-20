from django.shortcuts import render
from rest_framework import viewsets
from .models import Item 
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated 
from .permissions import IsAdmin 
from rest_framework import generics 
from .serializers import RegisterSerializer, CustomUserSerializer, LogoutSerializer
from django.contrib.auth import get_user_model 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model() 

class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemViewSet(viewsets.ModelViewSet): 
    queryset = Item.objects.all() 
    serializer_class = ItemSerializer 

    def get_permissions(self): 
        if self.request.method in ['POST', 'PUT', 'DELETE']: 
            return [IsAuthenticated(), IsAdmin()] 
        return [IsAuthenticated()] 


class RegisterView(generics.CreateAPIView): 
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer 
    
    
class LogoutView(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]  # Allow logout without authentication

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debugging

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                print("Logout error:", str(e))  # Debugging
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)