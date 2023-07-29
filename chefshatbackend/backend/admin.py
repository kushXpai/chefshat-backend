from django.contrib import admin
from .models import User, Dish, Ingredient, DishIngredient, DishStep, UserSavedRecipe, UserRatedRecipe

admin.site.register(User)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(DishIngredient)
admin.site.register(DishStep)
admin.site.register(UserSavedRecipe)
admin.site.register(UserRatedRecipe)