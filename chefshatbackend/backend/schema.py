import graphene
from graphene import List, Int
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import User, Dish, Ingredient, DishIngredient, DishStep, UserSavedRecipe, UserRatedRecipe, UserTip, UserRecentlyViewed, UserPantry, UserUpload
import datetime
from django.db.models import Count

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = "__all__"

class DishIngredientType(DjangoObjectType):
    class Meta:
        model = DishIngredient
        fields = "__all__"

class DishStepType(DjangoObjectType):
    class Meta:
        model = DishStep
        fields = "__all__"

class DishType(DjangoObjectType):
    class Meta:
        model = Dish
        fields = "__all__"

    ingredients = graphene.List(DishIngredientType, dishId=graphene.ID(required=True))

    savedCount = graphene.Int()  # Add this field

    def resolve_savedCount(self, info):
        return self.usersavedrecipe_set.count()

    def resolve_ingredients(self, info, dishId):
        return DishIngredient.objects.filter(dishId=dishId)
    
class UserSavedRecipeType(DjangoObjectType):
    class Meta:
        model = UserSavedRecipe
        fields = "__all__"

class UserRatedRecipeType(DjangoObjectType):
    class Meta:
        model = UserRatedRecipe
        fields = "__all__"

class UserTipType(DjangoObjectType):
    class Meta:
        model = UserTip
        fields = "__all__"

class UserPantryType(DjangoObjectType):
    class Meta:
        model = UserPantry
        fields = "__all__"

class UserRecentlyViewedType(DjangoObjectType):
    class Meta:
        model = UserRecentlyViewed
        fields = "__all__"

class UserUploadType(DjangoObjectType):
    class Meta:
        model = UserUpload
        fields = "__all__"





class SavedRecipeCountType(graphene.ObjectType):
    recipe_name = graphene.String()
    count = graphene.Int()





class Query(graphene.ObjectType):
    # USER
    displayUser = graphene.List(UserType)
    displayUserById = graphene.Field(UserType, id=graphene.ID(required=True))
    displayUserByMobileNumber = graphene.Field(UserType, mobileNumber=graphene.String(required=True))
    count_users_by_mobile_and_password = graphene.Int( mobile_number=graphene.String(required=True),password=graphene.String(required=True))
    get_user_id_by_mobile_and_password = graphene.Int(
        mobile_number=graphene.String(required=True),
        password=graphene.String(required=True)
    )
    displayUserByMobileNumberAndPassword = graphene.Field(UserType, mobileNumber=graphene.String(required=True), password=graphene.String(required=True))

    def resolve_displayUser(self, info):
        return User.objects.all()
    
    def resolve_displayUserById(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {id} does not exist.")
        
    def resolve_displayUserByMobileNumber(self, info, mobileNumber):
        try:
            return User.objects.get(mobileNumber=mobileNumber)
        except User.DoesNotExist:
            return None

    def resolve_count_users_by_mobile_and_password(self, info, mobile_number, password):
        user_count = User.objects.filter(mobileNumber=mobile_number, password=password).count()
        return user_count
    
    def resolve_displayUserByMobileNumberAndPassword(self, info, mobileNumber, password):
        try:
            return User.objects.get(mobileNumber=mobileNumber, password=password)
        except User.DoesNotExist:
            return None
    
    # activeUsers = graphene.List(UserType)

    # def resolve_activeUsers(self, info):
    #     # Calculate the activity score for each user
    #     users = User.objects.annotate(
    #         saved_recipe_count=Count('usersavedrecipe'),
    #         rated_recipe_count=Count('userratedrecipe'),
    #         upload_count=Count('userupload')
    #     )

    #     # Calculate the total activity score as the sum of saved recipes, rated recipes, and uploads
    #     users = users.annotate(
    #         total_activity_score=(
    #             users.saved_recipe_count +
    #             users.rated_recipe_count +
    #             users.upload_count
    #         )
    #     )

    #     # Sort users by their total activity score in descending order
    #     users = users.order_by('-total_activity_score')

    #     return users

    all_users_with_activity = graphene.List(UserType)

    def resolve_all_users_with_activity(self, info):
        # Implement your logic to calculate activity scores and sort users here
        # You'll need to query your database to retrieve user data and calculate scores
        users = User.objects.all()  # Replace with your actual query

        # Define a function to calculate the activity score for a user
        def calculate_activity_score(user):
            saved_recipe_count = user.usersavedrecipe_set.count()
            rated_recipe_count = user.userratedrecipe_set.count()
            upload_count = user.userupload_set.count()
            
            activity_score = saved_recipe_count + rated_recipe_count + upload_count
            
            return activity_score

        # Calculate activity scores for each user
        for user in users:
            user.activity_score = calculate_activity_score(user)

        # Sort users by their activity score in descending order
        sorted_users = sorted(users, key=lambda user: user.activity_score, reverse=True)

        return sorted_users



    # DISH 
    displayDish = graphene.List(DishType)
    displayDishById = graphene.Field(DishType, id=graphene.ID(required=True))
    displayDishByCuisine = graphene.List(DishType, dishCategoryCuisine=graphene.String(required=True))
    displayLastAddedDish = graphene.Field(DishType)
    displayDishesAddedLastWeek = graphene.List(DishType)
    displayDishesTrending = graphene.List(DishType)

    def resolve_displayDish(self, info):
        return Dish.objects.all()
    
    def resolve_displayDishById(self, info, id):
        try:
            return Dish.objects.get(id=id)
        except Dish.DoesNotExist:
            raise GraphQLError(f"Dish with ID {id} does not exist.")
        
    def resolve_displayDishByCuisine(self, info, dishCategoryCuisine):
        try:
            return Dish.objects.filter(dishCategoryCuisine=dishCategoryCuisine).order_by('-dishLastUpdate')
        except Dish.DoesNotExist:
            return None
        
    def resolve_displayLastAddedDish(self, info):
        try:
            return Dish.objects.latest('id')
        except Dish.DoesNotExist:
            return None
    
    def resolve_displayDishesAddedLastWeek(self, info):
        one_week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)
        
        return Dish.objects.filter(dishLastUpdate__gte=one_week_ago).order_by('-dishLastUpdate')
    
    def resolve_displayDishesTrending(self, info):
        return Dish.objects.all().order_by('-dishVisits')
    




    # INGREDIENT
    displayIngredient = graphene.List(IngredientType)
    displayIngredientById = graphene.Field(IngredientType, id=graphene.ID(required=True))
    displayIngredientByCategory = graphene.List(IngredientType, ingredientCategory=graphene.String(required=True))

    def resolve_displayIngredient(self, info):
        return Ingredient.objects.all()
    
    def resolve_displayIngredientById(self, info, id):
        try:
            return Ingredient.objects.get(id=id)
        except Ingredient.DoesNotExist:
            raise GraphQLError(f"Ingredient with ID {id} does not exist.")
        
    def resolve_displayIngredientByCategory(self, info, ingredientCategory):
        try:
            return Ingredient.objects.filter(ingredientCategory=ingredientCategory)
        except Ingredient.DoesNotExist:
            return None
        




    # DISH INGREDIENT
    displayDishIngredient = graphene.List(DishIngredientType)
    displayDishIngredientById = graphene.Field(DishIngredientType, dishId=graphene.ID(required=True))

    def resolve_displayDishIngredient(self, info):
        return DishIngredient.objects.all()
    
    def resolve_displayDishIngredientById(self, info, dishId):
        try:
            return DishIngredient.objects.filter(dishId=dishId)
        except DishIngredient.DoesNotExist:
            raise GraphQLError(f"Dish with ID {dishId} does not exist.")





    # DISH STEP
    displayDishStep = graphene.List(DishStepType)
    displayDishStepById = graphene.List(DishStepType, dishId=graphene.ID(required=True))

    def resolve_displayDishStep(self, info):
        return DishStep.objects.all()
    
    def resolve_displayDishStepById(self, info, dishId):
        try:
            return DishStep.objects.filter(dishId=dishId)
        except DishStep.DoesNotExist:
            raise GraphQLError(f"Dish with ID {dishId} does not exist.")




        
    # SAVED RECIPES
    displayUserSavedRecipe = graphene.List(UserSavedRecipeType)
    displayUserSavedRecipeById = graphene.List(UserSavedRecipeType, userId=graphene.ID(required=True))
    displayUserSavedRecipeByCourse = graphene.List(UserSavedRecipeType, userId=graphene.ID(required=True), userSavedRecipeCategory=graphene.String(required=True))

    def resolve_displayUserSavedRecipe(self, info):
        return UserSavedRecipe.objects.all().order_by('-recipeSaved')
    
    def resolve_displayUserSavedRecipeById(self, info, userId):
        try:
            return UserSavedRecipe.objects.filter(userId=userId).order_by('-recipeSaved')
        except UserSavedRecipe.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not have any saved recipes.")
        
    def resolve_displayUserSavedRecipeByCourse(self, info, userId, userSavedRecipeCategory):
        try:
            return UserSavedRecipe.objects.filter(userId=userId, userSavedRecipeCategory=userSavedRecipeCategory).order_by('-recipeSaved')
        except UserSavedRecipe.DoesNotExist:
            raise GraphQLError(f"User with {userSavedRecipeCategory} does not have any saved recipes.")


    displayNonVegetarianSavedRecipes = graphene.List(UserSavedRecipeType)
    displayVegetarianSavedRecipes = graphene.List(UserSavedRecipeType)

    def resolve_displayNonVegetarianSavedRecipes(self, info):
        non_vegetarian_dishes = Dish.objects.filter(dishCategoryDietary="nonvegetarian")
        non_vegetarian_saved_recipes = UserSavedRecipe.objects.filter(dishId__in=non_vegetarian_dishes).order_by('-recipeSaved')
        return non_vegetarian_saved_recipes

    def resolve_displayVegetarianSavedRecipes(self, info):
        vegetarian_dishes = Dish.objects.filter(dishCategoryDietary="vegetarian")
        vegetarian_saved_recipes = UserSavedRecipe.objects.filter(dishId__in=vegetarian_dishes).order_by('-recipeSaved')
        return vegetarian_saved_recipes
    

    allDishesWithSavedCounts = graphene.List(DishType)
    allVegetarianDishes = graphene.List(DishType)
    allNonVegetarianDishes = graphene.List(DishType)
    
    def resolve_allDishesWithSavedCounts(self, info):
        dishes = Dish.objects.annotate(savedCount=Count('usersavedrecipe'))
        dishes = sorted(dishes, key=lambda dish: dish.savedCount, reverse=True)      
        return dishes

    def resolve_allVegetarianDishes(self, info):
        vegetarian_dishes = Dish.objects.filter(dishCategoryDietary="vegetarian")
        vegetarian_dishes = vegetarian_dishes.annotate(savedCount=Count('usersavedrecipe'))
        vegetarian_dishes = sorted(vegetarian_dishes, key=lambda dish: dish.savedCount, reverse=True)
        return vegetarian_dishes

    def resolve_allNonVegetarianDishes(self, info):
        non_vegetarian_dishes = Dish.objects.filter(dishCategoryDietary="nonvegetarian")
        non_vegetarian_dishes = non_vegetarian_dishes.annotate(savedCount=Count('usersavedrecipe'))
        non_vegetarian_dishes = sorted(non_vegetarian_dishes, key=lambda dish: dish.savedCount, reverse=True)
        return non_vegetarian_dishes





    
    # RATED RECIPES
    displayUserRatedRecipe = graphene.List(UserRatedRecipeType)
    displayUserRatedRecipeById = graphene.List(UserRatedRecipeType, userId=graphene.ID(required=True))

    def resolve_displayUserRatedRecipe(self, info):
        return UserRatedRecipe.objects.all()
    
    def resolve_displayUserRatedRecipeById(self, info, userId):
        try:
            return UserRatedRecipe.objects.filter(userId=userId).order_by('-recipeRated')
        except UserRatedRecipe.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not have any rated recipes.")





    # TIPS 
    displayUserTip = graphene.List(UserTipType)
    displayUserTipById = graphene.List(UserTipType, userId=graphene.ID(required=True))

    def resolve_displayUserTip(self, info):
        return UserTip.objects.all()
    
    def resolve_displayUserTipById(self, info, userId):
        try:
            return UserTip.objects.filter(userId=userId).order_by('-recipeTiped')
        except UserTip.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not have any tip recipes.")
    



    # Recipe Searching
    searchDishesByIngredients = graphene.List(DishType, ingredients=graphene.List(graphene.String))

    def resolve_searchDishesByIngredients(self, info, ingredients):
        ingredient_objects = Ingredient.objects.filter(ingredientName__in=ingredients)

        dishes = Dish.objects.filter(dishingredient__ingredientId__in=ingredient_objects).distinct()

        for ingredient in ingredients:
            dishes = dishes.filter(dishingredient__ingredientId__ingredientName=ingredient)

        return dishes
  



    # Recently Viewed
    displayUserRecentlyViewed = graphene.List(UserRecentlyViewedType, userId=graphene.ID(required=True))

    def resolve_displayUserRecentlyViewed(self, info, userId):
        try:
            return UserRecentlyViewed.objects.filter(userId=userId).order_by('-recipeViewedTime')
        except UserRecentlyViewed.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} haven't seen any recipes.")
        



    # Pantry
    displayuserPantry = graphene.List(UserPantryType)
    displayuserPantryById = graphene.Field(UserPantryType, id=graphene.Int())
    displayuserPantryByDishId = graphene.List(UserPantryType,dishId=graphene.Int(),userId=graphene.Int())

    def resolve_displayuserPantry(self, info):
        return UserPantry.objects.all()

    def resolve_displayuserPantryById(self, info, id):
        return UserPantry.objects.get(pk=id)

    def resolve_displayuserPantryByDishId(self, info, dishId, userId):
        return UserPantry.objects.filter(dishId=dishId, userId=userId)
    



    # User Uploads
    displayUserUpload = graphene.List(UserUploadType)
    displayUserUploadById = graphene.List(UserUploadType, userId=graphene.ID(required=True))

    def resolve_displayUserUpload(self, info):
        return UserUpload.objects.all().order_by('-creationTime')
    
    def resolve_displayUserUploadById(self, info, userId):
        try:
            return UserUpload.objects.filter(userId=userId).order_by('-creationTime')
        except UserUpload.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not have any Uploads.")





class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        mobileNumber = graphene.String(required=True)
        profilePhoto = graphene.String(required=True)

    def mutate(self, info, username, password, mobileNumber, profilePhoto):
        from datetime import datetime
        dateOfBirth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
        user = User(username=username, password=password, mobileNumber=mobileNumber, profilePhoto=profilePhoto)
        user.save()
        return CreateUser(user=user)

class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        username = graphene.String()
        sex = graphene.String()
        address = graphene.String()
        emailAddress = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, user_id, username=None, sex=None, address=None, emailAddress=None):
        user = User.objects.get(pk=user_id)
        
        if username is not None:
            user.username = username
        if sex is not None:
            user.sex = sex
        if address is not None:
            user.address = address
        if emailAddress is not None:
            user.emailAddress = emailAddress

        user.save()

        return UpdateUserMutation(user=user)
        
class IncreaseDishVisits(graphene.Mutation):
    dish = graphene.Field(DishType)

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            dish = Dish.objects.get(id=id)
            dish.dishVisits += 1
            dish.save()
            return IncreaseDishVisits(dish=dish)
        except Dish.DoesNotExist:
            raise GraphQLError(f"Dish with ID {id} does not exist.")
        
class AddRecipeToSavedRecipe(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        dishId = graphene.ID(required=True)
        userSavedRecipeCategory = graphene.String(required=True)

    saved_recipe = graphene.Field(UserSavedRecipeType)

    def mutate(self, info, userId, dishId, userSavedRecipeCategory):
        try:
            user = User.objects.get(id=userId)
            dish = Dish.objects.get(id=dishId)
            
            saved_recipe = UserSavedRecipe.objects.filter(userId=user, dishId=dish).first()
            
            if saved_recipe:
                saved_recipe.userSavedRecipeCategory = userSavedRecipeCategory
                saved_recipe.save()
            else:
                saved_recipe = UserSavedRecipe(userId=user, dishId=dish, userSavedRecipeCategory=userSavedRecipeCategory)
                saved_recipe.save()
                
            return AddRecipeToSavedRecipe(saved_recipe=saved_recipe)
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not exist.")
        except Dish.DoesNotExist:
            raise GraphQLError(f"Dish with ID {dishId} does not exist.")

class RemoveRecipeFromSavedRecipe(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        dishId = graphene.ID(required=True)

    deletedCount = graphene.Int()

    def mutate(self, info, userId, dishId):
        try:
            user_saved_recipe = UserSavedRecipe.objects.get(userId=userId, dishId=dishId)
            user_saved_recipe.delete()
            return RemoveRecipeFromSavedRecipe(deletedCount=1)
        except UserSavedRecipe.DoesNotExist:
            return RemoveRecipeFromSavedRecipe(deletedCount=0)

from django.utils import timezone

class AddRecipeToRecentlyViewed(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        dishId = graphene.ID(required=True)

    recentlyViewed = graphene.Field(UserRecentlyViewedType)

    def mutate(self, info, userId, dishId):
        try:
            user = User.objects.get(id=userId)
            dish = Dish.objects.get(id=dishId)

            existing_entry = UserRecentlyViewed.objects.filter(userId=user, dishId=dish).first()

            if existing_entry:
                existing_entry.recipeViewedTime = timezone.now()
                existing_entry.save()
                return AddRecipeToRecentlyViewed(recentlyViewed=existing_entry)

            viewed_dishes_count = UserRecentlyViewed.objects.filter(userId=user).count()

            if viewed_dishes_count >= 5:
                oldest_entry = UserRecentlyViewed.objects.filter(userId=user).order_by('recipeViewedTime').first()
                oldest_entry.dishId = dish
                oldest_entry.recipeViewedTime = timezone.now()
                oldest_entry.save()
                return AddRecipeToRecentlyViewed(recentlyViewed=oldest_entry)
            else:
                recentlyViewed = UserRecentlyViewed(userId=user, dishId=dish, recipeViewedTime=timezone.now())
                recentlyViewed.save()
                return AddRecipeToRecentlyViewed(recentlyViewed=recentlyViewed)
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not exist.")
        except Dish.DoesNotExist:
            raise GraphQLError(f"Dish with ID {dishId} does not exist.")

class AddRecipeToRatedRecipe(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        dishId = graphene.ID(required=True)
        rating = graphene.String(required=True)

    ratingRecipe = graphene.Field(UserRatedRecipeType)

    def mutate(self, info, userId, dishId, rating):
        try:
            user = User.objects.get(id=userId)
            dish = Dish.objects.get(id=dishId)
            
            ratingRecipe = UserRatedRecipe.objects.filter(userId=user, dishId=dish).first()
            
            if ratingRecipe:
                ratingRecipe.rating = rating
                ratingRecipe.save()
            else:
                ratingRecipe = UserRatedRecipe(userId=user, dishId=dish, rating=rating)
                ratingRecipe.save()
                
            return AddRecipeToRatedRecipe(ratingRecipe=ratingRecipe)
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {userId} does not exist.")
        except Dish.DoesNotExist:
            raise GraphQLError(f"Dish with ID {dishId} does not exist.")

class AddOrUpdateUserPantry(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        dishId = graphene.ID(required=True)
        ingredientId = graphene.ID(required=True)

    userPantry = graphene.Field(UserPantryType)

    def mutate(self, info, userId, dishId, ingredientId):
        userPantry = userPantry.objects.filter(
            userId=userId,
            dishId=dishId,
            ingredientId=ingredientId
        ).first()

        if userPantry:
            userPantry.save()
        else:
            userPantry = userPantry(
                userId=userId,
                dishId=dishId,
                ingredientId=ingredientId
            )
            userPantry.save()

        return AddOrUpdateUserPantry(userPantry=userPantry)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUserMutation.Field()

    increase_dishVisits = IncreaseDishVisits.Field()

    add_recipe_to_saved_recipes = AddRecipeToSavedRecipe.Field()
    remove_recipe_from_saved_recipes = RemoveRecipeFromSavedRecipe.Field()

    add_recipe_to_recently_viewed = AddRecipeToRecentlyViewed.Field()

    add_recipe_to_rated_recipe = AddRecipeToRatedRecipe.Field()

    add_or_update_user_pantry = AddOrUpdateUserPantry.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)