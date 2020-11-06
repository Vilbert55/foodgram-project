from django.shortcuts import render, get_object_or_404
from .models import Ingredient


class IngredientsValid():
    def __init__(self, request):
        self.data = dict(request.POST.items())
        self.repeating_elements = []
            
        self.items = {}        

        for key in self.data:
            if 'idIngredient' in key:
                ingr_id = int(self.data[key])
                
                ingr_number = key.lstrip('idIngredient_')
                ingr_qty = int(self.data[f'valueIngredient_{ingr_number}'])
                if not self.items.get(ingr_id):
                    self.items[ingr_id] = ingr_qty
                else:
                    ingredient_obj = get_object_or_404(Ingredient, pk=ingr_id)
                    self.repeating_elements.append(ingredient_obj.title)

    def errors(self):
        if not self.items:
            return 'Вы не добавили ни одного ингредиента'
        if self.repeating_elements:
            elements = ', '.join(self.repeating_elements)
            return (f'В рецепте дублируются ингредиенты: {elements}')
        return False

