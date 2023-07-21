import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import User, Dish, Ingredient, DishIngredient
import datetime

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

class DishType(DjangoObjectType):
    class Meta:
        model = Dish
        fields = "__all__"

    ingredients = graphene.List(DishIngredientType, dishId=graphene.ID(required=True))

    def resolve_ingredients(self, info, dishId):
        return DishIngredient.objects.filter(dishId=dishId)

class Query(graphene.ObjectType):
    # USER
    displayUser = graphene.List(UserType)
    displayUserById = graphene.Field(UserType, id=graphene.ID(required=True))
    displayUserByMobileNumber = graphene.Field(UserType, mobileNumber=graphene.String(required=True))

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

    # DISH 
    displayDish = graphene.List(DishType)
    displayDishById = graphene.Field(DishType, id=graphene.ID(required=True))
    displayDishByCuisine = graphene.List(DishType, cuisine=graphene.String(required=True))
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
        
    def resolve_displayDishByCuisine(self, info, dishCuisine):
        try:
            return Dish.objects.filter(dishCuisine=dishCuisine).order_by('-dishLastUpdate')
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
        
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        sex = graphene.String(required=True)
        mobileNumber = graphene.String(required=True)
        emailAddress = graphene.String(required=True)
        dateOfBirth = graphene.String(required=True)
        address = graphene.String(required=True)
        profilePhoto = graphene.String(required=True)

    def mutate(self, info, username, sex, mobileNumber, emailAddress, dateOfBirth, address, profilePhoto):
        from datetime import datetime
        dateOfBirth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
        user = User(username=username, sex=sex, mobileNumber=mobileNumber, emailAddress=emailAddress, dateOfBirth=dateOfBirth, address=address, profilePhoto=profilePhoto)
        user.save()
        return CreateUser(user=user)
    
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

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

    increase_dishVisits = IncreaseDishVisits.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)