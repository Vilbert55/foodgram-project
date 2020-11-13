from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (IngredientListView, api_purchase_detail,
                    api_favorite_detail, api_follow_detail)


router = DefaultRouter()


router.register(r'ingredients', IngredientListView)


urlpatterns = [
    path('<int:recipe_id>/purchases/', api_purchase_detail),
    path('<int:recipe_id>/favorites/', api_favorite_detail),
    path('<int:cook_id>/subscriptions/', api_follow_detail),
]

urlpatterns += router.urls
