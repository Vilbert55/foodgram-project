from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (IngredientListView, api_purchase_detail,
                    api_favorite_detail, api_follow_detail)


router = DefaultRouter()


router.register(r'ingredients', IngredientListView)

urlpatterns = [
    path('purchases/<recipe_id>', api_purchase_detail),
    path('favorites/<recipe_id>', api_favorite_detail),
    path('subscriptions/<cook_id>', api_follow_detail),
]

urlpatterns += router.urls
