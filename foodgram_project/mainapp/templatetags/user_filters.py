from django import template

from mainapp.models import Follow, Purchase, Favorite, Recipe


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='is_follow')
def is_follow(cook, consumer):
    if not consumer.is_authenticated:
        return False
    return Follow.objects.filter(consumer=consumer, cook=cook).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    if not user.is_authenticated:
        return False
    return Favorite.objects.select_related('recipe').filter(
        user=user, recipe=recipe).exists()


@register.filter(name='is_purchase')
def is_purchase(recipe, buyer):
    if not buyer.is_authenticated:
        return False
    return Purchase.objects.select_related('recipe').filter(
        buyer=buyer, recipe=recipe).exists()


@register.filter(name='get_recipes')
def get_recipes(cook):
    return Recipe.objects.select_related('author').filter(author=cook)[:3]


@register.filter(name='get_count_recipes')
def get_count_recipes(cook):
    count = cook.recipes_author.count() - 3
    if count < 4:
        return False

    if count % 10 == 1 and count % 100 != 11:
        end = 'рецепт'
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        end = 'рецепта'
    else:
        end = 'рецептов'

    return f'Еще {count} {end}...'
