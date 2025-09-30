from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from .permissions import IsOwner
class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()               # base queryset (will be filtered in get_queryset)
    serializer_class = TaskSerializer            # which serializer to use for (de)serializing Task instances
    permission_classes = [IsAuthenticated,IsOwner]      # only logged-in users can access these endpoints

    # Optional: enable common filtering/searching/ordering (no extra imports here because configured in settings)
    filterset_fields = ['completed']            # lets clients filter with ?completed=true
    search_fields = ['title', 'description']    # lets clients search with ?search=word
    ordering_fields = ['created_at', 'updated_at']  # lets clients order with ?ordering=created_at

    def get_queryset(self):
        # self.request.user is the user from the JWT (or session) making the request
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]   # anyone (including anonymous) can register