from django.urls import path

from .views import (
    index, profile,
    recipe_view, recipe_edit,
    recipe_delete, purchases_list,
    favorite_list, follow_list,
    add_recipe, txt_upload)


urlpatterns = [
    path('', index, name='index'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('recipes/<str:username>/', profile, name='profile'),
    path('recipes/<str:username>/<int:recipe_id>/',
         recipe_view, name='recipe'),
    path('recipes/<str:username>/<int:recipe_id>/edit/',
         recipe_edit, name='recipe_edit'),
    path('recipes/<str:username>/<int:recipe_id>/delete/',
         recipe_delete, name='recipe_delete'),
    path('purchases/', purchases_list, name='purchases_list'),
    path('favorite/', favorite_list, name='favorite_list'),
    path('follows/', follow_list, name='follows'),
    path('getproducts/', txt_upload, name='getproducts')
]
