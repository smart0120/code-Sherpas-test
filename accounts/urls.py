from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet, index

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
]
