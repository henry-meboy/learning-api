from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Quote
from .serializers import QuoteSerializer, UserSignupSerializer
from .permissions import IsOwnerOrReadOnly
import random

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_view(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuoteViewSet(viewsets.ModelViewSet):
    """
    Provides: list, create, retrieve, update, destroy (all protected)
    plus: GET /api/quotes/random/ (public)
    """
    queryset = Quote.objects.all().order_by('-created_at')
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny], url_path='random')
    def random_quote(self, request):
        qs = Quote.objects.all()
        if not qs.exists():
            return Response({'message': 'No quotes yet'}, status=status.HTTP_200_OK)
        quote = random.choice(list(qs))
        serializer = self.get_serializer(quote)
        return Response(serializer.data)
