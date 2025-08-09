from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, signup_view

router = DefaultRouter()
router.register(r'quotes', QuoteViewSet, basename='quote')

urlpatterns = [
    path('signup/', signup_view, name='signup'),
]

urlpatterns += router.urls
