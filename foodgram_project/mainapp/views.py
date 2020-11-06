from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model, decorators
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Ingredient, Recipe, RecipeIngredient
from .forms import RecipeForm
from .utils import IngredientsValid

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
    food_time = request.GET.get('filter')
    
    #if food_time == 'breakfest':
        #recipe_list = Recipe.objects.filter(breakfest=True).order_by('-pub_date')
    #elif food_time == 'lunch':
        #recipe_list = Recipe.objects.filter(lunch=True).order_by('-pub_date')
    #elif food_time == 'dinner':
        #recipe_list = Recipe.objects.filter(dinner=True).order_by('-pub_date')
    #else:
        #recipe_list = Recipe.objects.order_by('-pub_date').all()

    food = {
        'breakfest': (True, False),
        'lunch': (True, False),
        'dinner': (True, False)
    }

    if food_time in food:
        food[food_time] = (True,)

    recipe_list = Recipe.objects.filter(
        breakfest__in=food['breakfest'],
        lunch__in=food['lunch'],
        dinner__in=food['dinner']).order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    #if request.user.is_authenticated:
    return render(request, 'indexAuth3.html', {'page': page, 'paginator': paginator, 'food_time':food_time})
    #return render(request, 'indexNotAuth.html')

def add_recipe(request):
       
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
            l=2
            for pk in data:
                ingredient_obj = get_object_or_404(Ingredient, pk=pk)
                ingredient_recipe = RecipeIngredient(ingredient=ingredient_obj, recipe=recipe, qty=data[pk])
                ingredient_recipe.save()
            form.save_m2m()
            return redirect('index')
        return render(request, 'formRecipe.html', {'form':form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form':form})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)

    inrgedients = RecipeIngredient.objects.filter(recipe_id=recipe.pk)

    return render(request, 'singlePage.html', {'recipe':recipe, 'username':author, 'ingredients':inrgedients})

