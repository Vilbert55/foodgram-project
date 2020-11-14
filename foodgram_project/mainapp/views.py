from django.contrib.auth import get_user_model, decorators
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Sum

from .models import Ingredient, Recipe, RecipeIngredient, Follow
from .forms import RecipeForm
from .utils import IngredientsValid, food_time_filter


User = get_user_model()


def index(request):

    recipes = Recipe.objects.select_related('author').all()
    recipes, food_time = food_time_filter(request, recipes)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'indexAuth3.html', {
        'page': page,
        'paginator': paginator,
        'food_time': food_time})


def profile(request, username):

    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.select_related(
        'author').filter(author_id=author.pk)
    recipes, food_time = food_time_filter(request, recipes)
    recipe_count = recipes.count()
    followers_count = Follow.objects.filter(cook=author).count()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'authorRecipe.html',
                  {'author': author,
                   'page': page,
                   'paginator': paginator,
                   'recipe_count': recipe_count,
                   'followers_count': followers_count,
                   'food_time': food_time})


@decorators.login_required
def purchases_list(request):
    bought_recipes = Recipe.objects.filter(
        purchases__buyer__pk=request.user.id)
    return render(request, 'shopList.html', {'recipes': bought_recipes})


@decorators.login_required
def favorite_list(request):
    favorite_recipes = Recipe.objects.select_related(
        'author').filter(favorites__user__pk=request.user.id)
    recipes, food_time = food_time_filter(request, favorite_recipes)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'favorite.html', {
        'page': page,
        'paginator': paginator,
        'food_time': food_time})


@decorators.login_required
def follow_list(request):
    cooks = User.objects.filter(cook__consumer__pk=request.user.id)

    paginator = Paginator(cooks, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'page': page,
        'paginator': paginator,
        'cooks_count': cooks.count})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    inrgedients = RecipeIngredient.objects.filter(recipe_id=recipe.pk)
    return render(request, 'singlePage.html', {
        'recipe': recipe,
        'username': username,
        'ingredients': inrgedients})


@decorators.login_required
def add_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        ingredients = IngredientsValid(request)
        if ingredients.errors():
            form.add_error(None, ingredients.errors())

    if form.is_valid():
        form.instance.author = request.user
        recipe = form.save(commit=False)
        recipe.save()
        data = ingredients.items
        for pk in data:
            ingredient_obj = get_object_or_404(Ingredient, pk=pk)
            ingredient_recipe = RecipeIngredient(
                ingredient=ingredient_obj, recipe=recipe, qty=data[pk])
            ingredient_recipe.save()
        form.save_m2m()
        return redirect('index')

    return render(request, 'formCreateRecipe.html', {'form': form})


@decorators.login_required
def recipe_edit(request, username, recipe_id):
    recipe_obj = get_object_or_404(
        Recipe, pk=recipe_id, author__username=username)
    ingredients_objs = RecipeIngredient.objects.filter(recipe=recipe_obj)

    if request.user != recipe_obj.author and not request.user.is_superuser:
        return redirect('recipe', username=username, recipe_id=recipe_id)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe_obj)

    if request.method == 'POST':
        ingredients = IngredientsValid(request)
        if ingredients.errors():
            form.add_error(None, ingredients.errors())

    if form.is_valid():
        recipe_obj = form.save(commit=False)
        recipe_obj.save()
        RecipeIngredient.objects.filter(recipe=recipe_obj).delete()
        data = ingredients.items
        for pk in data:
            ingredient_obj = get_object_or_404(Ingredient, pk=pk)
            ingredient_recipe = RecipeIngredient(
                ingredient=ingredient_obj, recipe=recipe_obj, qty=data[pk])
            ingredient_recipe.save()
        form.save_m2m()
        return redirect('index')

    return render(request, 'formChangeRecipe.html', {
        'form': form,
        'recipe_obj': recipe_obj,
        'ingredients_objs': ingredients_objs})


@decorators.login_required
def recipe_delete(request, username, recipe_id):
    recipe_obj = get_object_or_404(
        Recipe, author__username=username, pk=recipe_id)

    if request.method == 'POST':
        if recipe_obj.author == request.user or request.user.is_superuser:
            recipe_obj.delete()
        return redirect('index')
    else:
        return render(request, 'DeleteSubmit.html', {
            'recipe_id': recipe_id,
            'username': username,
            'recipe_obj': recipe_obj})


@decorators.login_required
def txt_upload(request):
    recipes = Recipe.objects.filter(purchases__buyer=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(
        total_qty=Sum('recipe__qty')
    )
    file_data = ''

    for i in ingredients:
        line = ' '.join(str(value) for value in i.values())
        file_data += line + '\n'

    response = HttpResponse(
        file_data, content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="products.txt"'
    return response
