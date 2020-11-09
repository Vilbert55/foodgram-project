from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipes/<username>/', views.profile, name='profile'),
    path('recipes/<username>/<int:recipe_id>/',
         views.recipe_view, name='recipe'),
    path('recipes/<username>/<int:recipe_id>/edit/',
         views.recipe_edit, name='recipe_edit'),
    path('recipes/<username>/<int:recipe_id>/delete/',
         views.recipe_delete, name='recipe_delete'),
    path('purchases/', views.purchases_list, name='purchases_list'),
    path('favorite/', views.favorite_list, name='favorite_list'),
    path('follows/', views.follow_list, name='follows'),
    path('load_from_json/', views.ingredients),
    path('getproducts/', views.txt_upload, name='getproducts')
]
