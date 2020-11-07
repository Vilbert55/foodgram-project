from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientListView, PurchaseViewSet

router = DefaultRouter()


router.register(r'ingredients', IngredientListView)
router.register(r'(?P<recipe_id>\d+)/purchases', PurchaseViewSet)

urlpatterns = router.urls