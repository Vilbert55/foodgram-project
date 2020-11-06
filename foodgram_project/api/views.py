from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics, filters, mixins, viewsets, serializers
from rest_framework.utils import json

from mainapp.models import Recipe, Ingredient
from .serializers import IngredientSerializer, RecipeSerializer






class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    #permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title',]



class RecipeViewSet(viewsets.ModelViewSet): 
    queryset = Recipe.objects.all() 
    serializer_class = RecipeSerializer 
        
    #permission_classes = [AdminOrReadOnly,]
    def perform_update(self, serializer):        
        user = self.request.user
        recipe = 'хз пока как достать'
        if Recipe.objects.filter(pk=recipe.pk, owners=user).exists(): 
            raise serializers.ValidationError('Already purchase')
        serializer.save(owners=user)


