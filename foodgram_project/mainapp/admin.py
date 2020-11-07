from django.contrib import admin

from .models import Ingredient, RecipeIngredient, Recipe, Purchase, Favorite, Follow


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('pk', 'title', 'dimension', 'description')
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('pk', 'title', 'description', 'author')
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'qty', 'recipe')
    search_fields = ('ingredient',)
    empty_value_display = '-empty-'


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'buyer', 'recipe')
    search_fields = ('buyer',)
    empty_value_display = '-empty-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-empty-'
    

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'consumer', 'cook')
    search_fields = ('consumer',)
    empty_value_display = '-empty-'
