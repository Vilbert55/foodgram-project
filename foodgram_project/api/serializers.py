from rest_framework import serializers
from django.contrib.auth import get_user_model

from mainapp.models import Ingredient, Recipe, Purchase


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredient


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()
    class Meta:
        fields = '__all__'
        model = Purchase
    