from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics, filters, mixins, viewsets, serializers
from rest_framework.utils import json
from rest_framework.response import Response

from mainapp.models import Recipe, Ingredient, Purchase
from .serializers import IngredientSerializer, PurchaseSerializer






class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    #permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title',]






class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    #permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnly, ]

    #def get_queryset(self):
        #queryset = self.queryset.filter(title_id=self.kwargs.get('title_id'))
        #return queryset

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('title_id')
        recipe = generics.get_object_or_404(Recipe, pk=recipe_id)
        user = self.request.user
        if Purchase.objects.filter(buyer=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already purcesed')
        serializer.save(buyer=user, recipe=recipe)
        return Response({'success': True})
        
        


