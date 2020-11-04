from rest_framework import serializers

from mainapp.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient