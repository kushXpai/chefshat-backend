from django.db import models

class FileField(models.FileField):
    def value_to_string(self, obj):
        return obj.file.url

def defaultProfile():
    if User.sex == 'MALE':
        return 'https://i.pinimg.com/originals/ba/be/1f/babe1f8eddf93fbcb3d1802bc1b65fe4.png'
    elif User.sex == 'FEMALE':
        return 'https://i.pinimg.com/originals/be/84/e8/be84e8c7ce61aaec1426b217d2b0ed3b.png'
    
def defaultDishImage():
    return 'https://www.istockphoto.com/vector/hand-drawn-vector-seamless-pattern-with-sketch-dairy-products-on-a-blackboard-gm1224636004-360176253?phrase=black%20and%20white%20dish'

def defaultIngredientImage():
    return 'ingredientImages/default.png'
    
class User(models.Model):
    SEX_CHOICES = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
    )

    username = models.CharField(max_length=255)
    profilePhoto = FileField(upload_to='userProfilePhotos/',default=defaultProfile, null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    mobileNumber = models.CharField(max_length=10)
    emailAddress = models.EmailField(max_length=100)
    dateOfBirth = models.DateField()
    address = models.TextField(max_length=1000)
    followers = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)
    creationTime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} : {self.username}"

class Dish(models.Model):

    COURSE_CHOICES = (
        ("appetizers", "Appetizers"),
        ("entree", "Entree"),
        ("desserts", "Desserts"),
        ("sides", "Sides"),
        ("snacks", "Snacks"),
    )
    CUISINE_CHOICES = (
        ("indian", "Indian"),
        ("italian", "Italian"),
        ("spanish", "Spanish"),
        ("chinese", "Chinese"),
        ("japanese", "Japanese"),
        ("states", "States"),
        ("british", "British"),
    )
    DIETARY_CHOICES = (
        ("vegetarian", "Vegetarian"),
        ("vegan", "Vegan"),
        ("nonvegetarian", "Non Vegetarian"),
        ("pescatarian", "Pescatarian"),
    )
    ALLERGEN_CHOICES = (
        ("nut", "Contains Nuts"),
        ("shellfish", "Contains Shellfish"),
        ("soy", "Contains Soy"),
        ("egg", "Contains Egg"),
        ("dairy", "Contains Dairy Products"),
        ("none", "None"),
    )
    SPICENESS_LEVEL_CHOICES = (
        ("mild", "Mild"),
        ("medium", "Medium"),
        ("spicy", "Spicy"),
        ("extraspicy", "Extra Spicy"),
    )
    SEASON_CHOICES = (
        ("spring", "Spring"),
        ("summer", "Summer"),
        ("autumn", "Autumn"),
        ("winter", "Winter"),
        ("all", "All"),
    )

    dishName = models.CharField(max_length = 200)
    dishCourse = models.CharField(max_length= 200, choices = COURSE_CHOICES)
    dishCuisine = models.CharField(max_length= 200, choices = CUISINE_CHOICES)
    dishCategoryDietary = models.CharField(max_length= 200, choices = DIETARY_CHOICES)
    dishCategoryAllergen = models.CharField(max_length= 200, choices = ALLERGEN_CHOICES)
    dishCategorySpicenessLevel = models.CharField(max_length= 200, choices = SPICENESS_LEVEL_CHOICES)
    dishCategorySeason = models.CharField(max_length= 200, choices = SEASON_CHOICES)
    dishImage = FileField(upload_to='dishImages/',default=defaultDishImage, null=True, blank=True)
    dishDescription = models.CharField(max_length = 10000)
    dishRating = models.DecimalField(max_digits=3, decimal_places=2)
    dishTotalTime = models.CharField(max_length =20)
    dishPreparationTime = models.CharField(max_length = 20)
    dishCookingTime = models.CharField(max_length = 20)
    dishCalories = models.CharField(max_length = 20)
    dishProteins = models.CharField(max_length = 20)
    dishFats = models.CharField(max_length = 20)
    dishCarbohydrates = models.CharField(max_length = 20)
    dishFibres = models.CharField(max_length = 20)
    dishSugar = models.CharField(max_length = 20)
    dishSodium = models.CharField(max_length = 20)
    dishLastUpdate = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return f"{self.id} : {self.dishName}"
    
class Ingredient(models.Model):

    CATEGORY_CHOICES = (
        ("vegetables", "Vegetables"),
        ("mushrooms", "Mushrooms"),
        ("fruits", "Fruits"),
        ("berries", "Berries"),
        ("nutsseeds", "Nuts N Seeds"),
        ("cheeses", "Cheeses"),
        ("dairy", "Dairy"),
        ("dairyfree", "Dairy Free"),
        ("eggs", "Eggs"),
        ("pasta", "Pasta"),
        ("meat", "Meat"),
        ("meatsubstitutes", "Meat Substitutes"),
        ("poulty", "Poulty"),
        ("fish", "Fish"),
        ("shellfish", "Shellfish"),
        ("herbsspices", "Herbs N Spices"),
        ("sugarsweetners", "Sugar N Sweetners"),
        ("seasoning", "Seasonings"),
        ("baking", "Baking"),
        ("grains", "Grains"),
        ("legumes", "Legumes"),
        ("breads", "Breads"),
        ("oilsfats", "Oils N Fats"),
        ("dressingsvinegars", "Dressings N Vinegars"),
        ("condiments", "Condiments"),
        ("canned", "Canned Foods"),
        ("saucesspreadsdips", "Sauces, Spreads N Dips"),
        ("stewsstocks", "Stews N Stocks"),
        ("dessertssweets", "Desserts N Sweets"),
        ("alcohol", "Alcohol"),
        ("breverages", "Breverages"),
    )

    ingredientName = models.CharField(max_length = 200)
    ingredientImage = FileField(upload_to='ingredientImages/',default=defaultIngredientImage, null=True, blank=True)
    ingredientCategory = models.CharField(max_length =50, choices = CATEGORY_CHOICES)
    ingredientPantryEssentials = models.BooleanField(default = False)


    def __str__(self) -> str:
        return f"{self.id} : {self.ingredientName}"
    
class DishIngredient(models.Model):

    dishId = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredientId = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    dishIngredientQuantity = models.IntegerField()
    dishIngredientQuantityUnit = models.CharField(max_length = 200)  

    def __str__(self) -> str:
        return f"{self.dishId} : {self.ingredientId}"
