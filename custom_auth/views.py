from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, LoginSerializer,RefreshTokenSerializer,CustomTokenObtainPairSerializer
from .models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions


@permission_classes([IsAuthenticated])
class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer

@permission_classes([IsAuthenticated])
class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = CustomUserSerializer

@permission_classes([IsAuthenticated])
class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        staffid = serializer.validated_data['staffid']
        password = serializer.validated_data['password']
        try:
            user = CustomUser.objects.get(staffid=staffid)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            access = CustomTokenObtainPairSerializer.get_token(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(access.access_token),
                'is_staff': user.is_staff,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAuthenticated])
class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)

@permission_classes([IsAuthenticated])
class RefreshTokenView(generics.CreateAPIView):
    serializer_class = RefreshTokenSerializer  # Use the appropriate serializer for refresh token
    def create(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        serializer = self.get_serializer(data={'refresh': refresh})
        if serializer.is_valid():
            refresh_token = serializer.validated_data.get('refresh')
            access_token = RefreshToken(refresh_token).access_token
          
            response_data = {
                'access': str(access_token),
            }
            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)