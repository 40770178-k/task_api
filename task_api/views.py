from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Task objects.
    ModelViewSet provides list/create/retrieve/update/destroy actions.
    """
    queryset = Task.objects.all()               # base queryset (will be filtered in get_queryset)
    serializer_class = TaskSerializer            # which serializer to use for (de)serializing Task instances
    permission_classes = [IsAuthenticated]      # only logged-in users can access these endpoints

    # Optional: enable common filtering/searching/ordering (no extra imports here because configured in settings)
    filterset_fields = ['completed']            # lets clients filter with ?completed=true
    search_fields = ['title', 'description']    # lets clients search with ?search=word
    ordering_fields = ['created_at', 'updated_at']  # lets clients order with ?ordering=created_at

    def get_queryset(self):
        """
        Return only tasks that belong to the authenticated user.
        This prevents users from seeing other users' tasks.
        """
        # self.request.user is the user from the JWT (or session) making the request
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Called when a new Task is created (POST /api/tasks/).
        We set the 'user' field to the current user automatically.
        """
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    """
    Simple registration endpoint for creating new users.
    Uses RegisterSerializer which must create the user (handle password hashing).
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]   # anyone (including anonymous) can register