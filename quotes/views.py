from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Quote
from .serializers import QuoteSerializer, UserSignupSerializer
from .permissions import IsOwnerOrReadOnly
import random

# drf-yasg swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

@swagger_auto_schema(
    method='post',
    request_body=UserSignupSerializer,
    responses={
        201: openapi.Response(description="User created successfully"),
        400: "Validation errors"
    }
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_view(request):
    """
    Endpoint to register a new user.
    """
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuoteViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, destroy for Quotes (authentication required),
    plus a public GET /api/quotes/random/ to get a random quote.
    """
    queryset = Quote.objects.all().order_by('-created_at')
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        method='get',
        operation_summary="Get a random quote",
        operation_description="Retrieve a single random quote from the database.",
        responses={200: QuoteSerializer()}
    )
    @action(detail=False, methods=['GET'], permission_classes=[permissions.AllowAny], url_path='random')
    def random_quote(self, request):
        qs = Quote.objects.all()
        if not qs.exists():
            return Response({'message': 'No quotes yet'}, status=status.HTTP_200_OK)
        quote = random.choice(list(qs))
        serializer = self.get_serializer(quote)
        return Response(serializer.data)
