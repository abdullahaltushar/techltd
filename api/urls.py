from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesViewSet
from .views import SalesReport
router = DefaultRouter()
router.register(r'sales', SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate_report/', SalesReport.as_view()),
]
