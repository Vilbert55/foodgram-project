from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'breakfest', 'lunch', 'dinner', 'ingredients', 'cooking_time', 'image',]