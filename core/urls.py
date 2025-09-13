from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, RunViewSet

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'runs', RunViewSet, basename='run')

urlpatterns = [
    path('', include(router.urls)),
]