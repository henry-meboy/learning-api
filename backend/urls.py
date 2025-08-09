from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quotes.views import QuoteViewSet, signup_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger / OpenAPI
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'quotes', QuoteViewSet, basename='quote')

schema_view = get_schema_view(
   openapi.Info(
      title="Quotes API",
      default_version='v1',
      description="API for creating and fetching quotes (learning project)",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup_view, name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),

    # Swagger UI
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
