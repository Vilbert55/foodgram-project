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

    def validate(self, data):
        super().validate(data)
        user = self.context.get('request_user')
        recipe = self.context.get('request_recipe')
        if Purchase.objects.filter(buyer=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already purchased')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Favorite

    def validate(self, data):
        super().validate(data)
        user = self.context.get('request_user')
        recipe = self.context.get('request_recipe')
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already added')
        return data


class FollowSerializer(serializers.ModelSerializer):
    consumer = serializers.StringRelatedField()
    cook = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Follow

    def validate(self, data):
        super().validate(data)
        consumer = self.context.get('request_consumer')
        cook = self.context.get('request_cook')
        if Follow.objects.filter(consumer=consumer, cook=cook).exists():
            raise serializers.ValidationError('Already follow')
        return data
