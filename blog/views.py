from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from rest_framework.exceptions import ValidationError

# Create your views here.

# registration
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
# login
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email,password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),  
            })
            
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
# user profile
class UserProfileView(CreateAPIView, RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile,created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def perform_create(self,serializer):
        if UserProfile.objects.filter(user=self.request.user).exists():
            raise ValidationError({'error':'Profile already exists'})
        
        serializer.save(user=self.request.user)