from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'breakfest',
                  'lunch', 'dinner', 'cooking_time', 'image', ]
