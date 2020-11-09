from rest_framework import generics, filters, mixins, viewsets, status

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

from mainapp.models import Recipe, Ingredient, Purchase, Follow, Favorite
from .serializers import (
    IngredientSerializer,
    PurchaseSerializer,
    FavoriteSerializer,
    FollowSerializer)
from django.db.utils import IntegrityError


User = get_user_model()


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]


@api_view(['POST', 'DELETE'])
def api_purchase_detail(request, recipe_id):
    recipe = generics.get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        serializer = PurchaseSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(buyer=request.user, recipe=recipe)
            except IntegrityError:  # если такая покупка уже есть
                Response({'success': False},
                         status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        purchase = generics.get_object_or_404(
            Purchase, buyer=request.user, recipe=recipe)
        purchase.delete()
        return Response({'success': True})


@api_view(['POST', 'DELETE'])
def api_favorite_detail(request, recipe_id):
    recipe = generics.get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user, recipe=recipe)
            except IntegrityError:
                Response({'success': False},
                         status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        favorite = generics.get_object_or_404(
            Favorite, user=request.user, recipe=recipe)
        favorite.delete()
        return Response({'success': True})


@api_view(['POST', 'DELETE'])
def api_follow_detail(request, cook_id):
    cook = generics.get_object_or_404(User, pk=cook_id)
    if request.method == 'POST':
        serializer = FollowSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(consumer=request.user, cook=cook)
            except IntegrityError:
                Response({'success': False},
                         status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        follow = generics.get_object_or_404(
            Follow, consumer=request.user, cook=cook)
        follow.delete()
        return Response({'success': True})
