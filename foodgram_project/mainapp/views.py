from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model, decorators
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Ingredient, Recipe, RecipeIngredient
from .forms import RecipeForm
from .utils import IngredientsValid, food_time_filter

from django.contrib.auth.decorators import user_passes_test


User = get_user_model()


@user_passes_test(lambda u: u.is_superuser)
def ingredients(request):
    import json
    from django.http import HttpResponse

    with open('ingredients.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        print('Новый ингридиент:',i)
        ingredient = Ingredient(title=i['title'], dimension=i['dimension'])
        ingredient.save()
    return HttpResponse('\n'.join(str(data)))

def index(request):
    #filters = FoodTimeFilter(request)
    recipes = Recipe.objects.select_related('author').order_by('-pub_date').all()
    #recipe_list = Recipe.objects.filter(
        #breakfest__in=filters.breakfest(),
        #lunch__in=filters.lunch(),
        #dinner__in=filters.dinner()).order_by('-pub_date').all()
    recipe_list, food_time = food_time_filter(request, recipes)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    #if request.user.is_authenticated:
    return render(request, 'indexAuth3.html', {'page': page, 'paginator': paginator, 'food_time':food_time})
    #return render(request, 'indexNotAuth.html')


def profile(request, username):

    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.select_related('author').filter(author_id=author.pk).order_by('-pub_date').all()
    recipe_list, food_time = food_time_filter(request, recipes)

    paginator = Paginator(recipe_list, 6)
    recipe_count = recipe_list.count
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    #following = False
    #if request.user.is_authenticated:
        #following = Follow.objects.filter(user=request.user, author=author).exists()
    return render(request, 'authorRecipe.html',
        {'author':author,
         'page':page,
         'paginator': paginator,
         'recipe_count':recipe_count,
         'food_time':food_time,
         'following':'пока не сделано' })


def purchases_list(request):

    #bought_recipes = request.user.purchases.all().values('recipe')
    bought_recipes = Recipe.objects.filter(purchases__buyer__pk=request.user.id).all()
    return render(request, 'shopList.html', {'recipes':bought_recipes})


def favorite_list(request):
    bought_recipes = Recipe.objects.filter(purchases__buyer__pk=request.user.id).all()
    return render(request, 'favorite.html', {'recipes':bought_recipes})


def add_recipe(request):
       
    if request.method == 'POST':
        author = request.user    
        ingredients = IngredientsValid(request)
        form = RecipeForm(request.POST or None, files=request.FILES or None, )
        if ingredients.errors():
            errors = ingredients.errors()
            form.add_error(None, errors)
            
        if form.is_valid():
            form.instance.author = author
            recipe = form.save(commit=False)
            recipe.save()
            data = ingredients.items
            for pk in data:
                ingredient_obj = get_object_or_404(Ingredient, pk=pk)
                ingredient_recipe = RecipeIngredient(ingredient=ingredient_obj, recipe=recipe, qty=data[pk])
                ingredient_recipe.save()
            form.save_m2m()
            del ingredients
            return redirect('index')
        del ingredients
        return render(request, 'formRecipe.html', {'form':form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form':form})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    inrgedients = RecipeIngredient.objects.filter(recipe_id=recipe.pk)
    return render(request, 'singlePage.html', {'recipe':recipe, 'username':author, 'ingredients':inrgedients})



def recipe_edit(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe_obj = get_object_or_404(Recipe, pk=recipe_id)

    if recipe_obj.author != request.user != user:
        return redirect('recipe', username=username, recipe_id=recipe_id)

    if request.method == 'POST':
        author = request.user    
        ingredients = IngredientsValid(request)
        form = RecipeForm(request.POST or None, files=request.FILES or None, )
        if ingredients.errors():
            errors = ingredients.errors()
            form.add_error(None, errors)
            
        elif form.is_valid():
            form.instance.author = author
            recipe = form.save(commit=False)
            recipe.save()
            data = ingredients.items            
            for pk in data:
                ingredient_obj = get_object_or_404(Ingredient, pk=pk)
                ingredient_recipe = RecipeIngredient(ingredient=ingredient_obj, recipe=recipe, qty=data[pk])
                ingredient_recipe.save()
            form.save_m2m()
            return redirect('index')
        return render(request, 'formRecipe.html', {'form':form})
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe_obj)
    return render(request, 'formRecipe.html', {'form':form, 'recipe_obj':recipe_obj})


