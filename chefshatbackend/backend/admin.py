from django.contrib import admin
from .models import User, Dish, Ingredient, DishIngredient, DishStep, UserSavedRecipe, UserRatedRecipe, UserTip, UserRecentlyViewed, UserPantry

admin.site.register(User)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(DishIngredient)
admin.site.register(DishStep)
admin.site.register(UserSavedRecipe)
admin.site.register(UserRatedRecipe)
admin.site.register(UserTip)
admin.site.register(UserRecentlyViewed)
admin.site.register(UserPantry)