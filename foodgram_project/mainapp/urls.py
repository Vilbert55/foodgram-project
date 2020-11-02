from django.urls import path
from . import views

urlpatterns = [
    path('add_recipe', views.add_recipe, name = 'add_recipe'),
    path('add_from_json/', views.ingredients),
    path('', views.index, name = 'index'),
    
]