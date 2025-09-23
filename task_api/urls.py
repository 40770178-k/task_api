from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import views
from .views import TaskViewSet, RegisterView

# Import JWT views (for authentication tokens)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router for automatically handling TaskViewSet routes
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')  # /api/tasks/

# Define all URL patterns
urlpatterns = [
    # User registration endpoint
    path('auth/register/', RegisterView.as_view(), name='register'),

    # JWT authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Expose router endpoints at root here; project urls already prefix with 'api/'
    path('', include(router.urls)),  
]
