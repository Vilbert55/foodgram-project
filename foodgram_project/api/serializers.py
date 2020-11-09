from rest_framework import serializers

from mainapp.models import Ingredient, Purchase, Favorite, Follow


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


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Favorite


class FollowSerializer(serializers.ModelSerializer):
    consumer = serializers.StringRelatedField()
    cook = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Follow
