from rest_framework import serializers
from django.contrib.auth import get_user_model

from mainapp.models import Ingredient, Recipe


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    owners = serializers.SlugRelatedField(slug_field='slug', queryset=User.objects.all(), many=True)
    class Meta:
        fields = ('owners',)
        model = Recipe
    