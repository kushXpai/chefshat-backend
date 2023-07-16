import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import User, Dish

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

class DishType(DjangoObjectType):
    class Meta:
        model = Dish
        fields = "__all__"

class Query(graphene.ObjectType):
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
        
    displayDish = graphene.List(DishType)
    displayDishById = graphene.Field(DishType, id=graphene.ID(required=True))
    displayDishByCuisine = graphene.List(DishType, cuisine=graphene.String(required=True))

    def resolve_displayDish(self, info):
        return Dish.objects.all()
    
    def resolve_displayDishById(self, info, id):
        try:
            return Dish.objects.get(id=id)
        except Dish.DoesNotExist:
            raise GraphQLError(f"Dish with ID {id} does not exist.")
        
    def resolve_displayDishByCuisine(self, info, cuisine):
        try:
            return Dish.objects.filter(cuisine=cuisine)
        except Dish.DoesNotExist:
            return None
        
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

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)