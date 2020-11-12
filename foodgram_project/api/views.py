from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

from mainapp.models import Recipe, Ingredient, Purchase, Follow, Favorite
from .serializers import (IngredientSerializer, PurchaseSerializer,
                          FavoriteSerializer, FollowSerializer)


User = get_user_model()


class IngredientListView(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]


@api_view(['POST', 'DELETE'])
def api_purchase_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        serializer = PurchaseSerializer(data=request.data, context={
            'request_user': request.user,
            'request_recipe': recipe})
        serializer.is_valid(raise_exception=True)
        serializer.save(buyer=request.user, recipe=recipe)
        return Response({'success': True}, status=HTTP_201_CREATED)

    if request.method == 'DELETE':
        get_object_or_404(
            Purchase, buyer=request.user, recipe=recipe).delete()

        return Response({'success': True})


@api_view(['POST', 'DELETE'])
def api_favorite_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data, context={
            'request_user': request.user,
            'request_recipe': recipe})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, recipe=recipe)
        return Response({'success': True}, status=HTTP_201_CREATED)

    if request.method == 'DELETE':
        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return Response({'success': True})


@api_view(['POST', 'DELETE'])
def api_follow_detail(request, cook_id):
    cook = get_object_or_404(User, pk=cook_id)
    if request.method == 'POST':
        serializer = FollowSerializer(data=request.data, context={
            'request_consumer': request.user,
            'request_cook': cook})
        serializer.is_valid(raise_exception=True)
        serializer.save(consumer=request.user, cook=cook)
        return Response({'success': True}, status=HTTP_201_CREATED)

    if request.method == 'DELETE':
        get_object_or_404(Follow, consumer=request.user, cook=cook).delete()
        return Response({'success': True})
