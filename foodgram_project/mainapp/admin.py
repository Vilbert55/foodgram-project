from django.contrib import admin

from .models import Ingredient, RecipeIngredient, Recipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension', 'description')
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'qty')
    search_fields = ('ingredient',)
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'author')
    search_fields = ('title',)
    empty_value_display = '-empty-'
