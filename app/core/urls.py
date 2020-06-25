from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, OrderViewSet, BillViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("orders", OrderViewSet, basename="orders")
router.register("bills", BillViewSet, basename="bills")

app_name = "core"

urlpatterns = [
    path("", include(router.urls)),
]