from django.urls import path
from .views import CustomUserCreateView, CustomUserDetailView, CustomUserListView, LoginView,VerifyTokenView
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    # path('edit_user/', CustomUserDetailView.as_view(), name='edit_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # CRUD operations for users
    path('users/', CustomUserListView.as_view(), name='user-list'),             # List and Create Users
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('verify/', VerifyTokenView.as_view(), name='verify-token'),
]
