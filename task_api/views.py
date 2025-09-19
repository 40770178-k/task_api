from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['completed']              # filter ?completed=true
    search_fields = ['title', 'description']      # ?search=buy
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        # Only return tasks belonging to the logged-in user
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # On create, set the user to the request user
        serializer.save(user=self.request.user)

# Simple registration endpoint
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

