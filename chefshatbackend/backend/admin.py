from django.contrib import admin
from .models import User, Dish, Ingredient, DishIngredient

admin.site.register(User)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(DishIngredient)