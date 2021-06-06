import user
import requests
from django.contrib.auth.models import User
from django.shortcuts import render , HttpResponse , redirect , HttpResponseRedirect
from django.http import JsonResponse
from datetime import datetime
from .models import Recipe , FoodList  ,Comment
from user.models import Profile
from .forms import FoodListForm , RecipeForm ,CommentForm

from django.utils import timezone

from datetime import datetime, timedelta

from .forms import FoodListForm , RecipeForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime 


# Create your views here.
def home(request):
    # result = 66+(13.7*user.weight)+(5*user.height)-(6.6*user.age)
    # print(result)
    foods = FoodList.objects.filter(date=datetime.date.today())
    # recipes = recipes.objects.filter(date__gte=datetime.date.today())
    recipes = Recipe.objects.order_by()[0:3]
    today = datetime.date.today()


    return render(request, 'home.html' , {"foods" : foods , "recipes":recipes , "today":today} )

# ----------- Recipies CRUD ----------- 
    
def recipes(request): 
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list,3)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page =1
    try:
        all_recipes = paginator.page(page)
    except(EmptyPage,InvalidPage):
        all_recipes = paginator.page(paginator.num_pages)

    return render(request , 'recipe/all_recipe.html' , 
    {"all_recipes" : all_recipes  })

@login_required()
def new_recipe(request):
	if request.method == "POST":
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.author = request.user
			obj.save()
			return redirect("/recipe")
	form = RecipeForm()
	template_name = "recipe/recipe_form.html"
	context = {
		"form":form
	}
	return render(request, template_name, context)

def show_recipe(request , pk):
    post=Recipe.objects.get(id=pk)
    id_=pk
    comments=Comment.objects.filter(post=post).order_by("-pk")
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True
    else:
        is_liked=False
    if request.method == 'POST':
	    cf = CommentForm(request.POST or None)
	    if cf.is_valid():
	        content = request.POST.get('content')
	        comment = Comment.objects.create(post = post, user = request.user, content = content)
	        comment.save()
	        return redirect(f'/recipe/{pk}')
    else:
        cf=CommentForm()

    context={
    'title': 'Recipe Details',
    'comments':comments,
    'id_':id_,
    'object':post,
    'is_liked':is_liked,
    'total_likes':post.likecount(),
    'comment_form':cf
    }
    return render(request, 'recipe/show_recipe.html',context)


@login_required()
def update_recipe(request,pk):
    update_recipe= Recipe.objects.get(pk=pk)
    form = RecipeForm(instance=update_recipe)
    if (request.method == "POST"):
        Update_recipe =RecipeForm(request.POST,instance=update_recipe) 
        if Update_recipe.is_valid() :
            Update_recipe.save()
            messages.add_message(request , messages.SUCCESS , "Recipe has been updated!")
            return redirect (f'/recipe/{pk}')

    update_recipe= Recipe.objects.get(pk=pk)
    form = RecipeForm(instance=update_recipe)
    return render(request , 'recipe/recipe_form.html' , 
    {"form" : form})

@login_required()
def delete_recipe(request , pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe.delete()
    messages.add_message(request , messages.SUCCESS , "Recipe has been successfullly deleted!")
    return redirect('/recipe')

# ----------- FoodList CRUD ----------- 

@login_required()
def foodlist(request  , date): 
    all_foodlist=FoodList.objects.order_by('-date')
    print(date.split('-'))
    convertdare =  datetime.date(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))
    yesterday =  convertdare  - timedelta(days=1) 
    tomorrow =  convertdare  + timedelta(days=1)       # all_foodlist = FoodList.objects.all().values_list()
    today_foods = []
    
    for food in all_foodlist:
        if (convertdare == food.date):
            today_foods.append(food)

    # print(today_foods)
    return render(request , 'foodlist/show_foodlist.html' , 
    # {"all_foodlist" : all_foodlist ,'today_foods':today_foods ,'next_food':next_food ,'prev_food':prev_food ,'today'})
    {"all_foodlist" : today_foods ,
    "yesterday" : yesterday , 
    'tomorrow' : tomorrow,
    "convertdare" :convertdare
    })


@login_required()
def new_foodlist(request):
    form = FoodListForm()
    today = datetime.date.today()

    if (request.method == "POST"):
        foodlist = FoodListForm(request.POST)
        if (foodlist.is_valid()):
            ingr = request.POST["meal_name"]
            quant = request.POST["quantity"]
            # url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={fish}&app_id=8dd6ffa9&app_key=2684fc8a5202887d5c7167103b71f982"
            url = f"https://api.edamam.com/api/nutrition-data?app_id=8dd6ffa9&app_key=2684fc8a5202887d5c7167103b71f982&ingr={quant}%20{ingr}"
            response = requests.request("GET", url)
            response_data = response.json()
            response_code = response.status_code
        
            foodlist = foodlist.save(commit=False)
            foodlist.user = request.user
            foodlist.total_calories = response_data["calories"]
            foodlist.total_fat = response_data["totalNutrientsKCal"]["FAT_KCAL"]["quantity"]
            foodlist.total_protein = response_data["totalNutrientsKCal"]["PROCNT_KCAL"]["quantity"]
            foodlist.total_carbs = response_data["totalNutrientsKCal"]["CHOCDF_KCAL"]["quantity"]

            if (foodlist.total_calories == 0):
                messages.add_message(request , messages.SUCCESS , "There is a mistake in the name")
                return render(request , 'foodlist/foodlist_form.html' , {'form' : form})
            else:
                foodlist.save()
                messages.add_message(request , messages.SUCCESS , "A new meal has been posted")
                return redirect(f'/foodlist/{today}')
        pass

    return render(request , 'foodlist/foodlist_form.html' , {'form' : form})

@login_required()
def update_foodlist(request,pk):
    update_foodlist= FoodList.objects.get(pk=pk)
    form = FoodListForm(instance=update_foodlist)
    today = datetime.date.today()
    if (request.method == "POST"):
        Update_foodlist =FoodListForm(request.POST,instance=update_foodlist)
        if Update_foodlist.is_valid() :
            ingr = request.POST["meal_name"]
            quant = request.POST["quantity"]
            url = f"https://api.edamam.com/api/nutrition-data?app_id=8dd6ffa9&app_key=2684fc8a5202887d5c7167103b71f982&ingr={quant}%20{ingr}"
            response = requests.request("GET", url)
            response_data = response.json()
            Update_foodlist = Update_foodlist.save(commit=False)
            Update_foodlist.total_calories = response_data["calories"]
            Update_foodlist.total_fat = response_data["totalNutrientsKCal"]["FAT_KCAL"]["quantity"]
            Update_foodlist.total_protein = response_data["totalNutrientsKCal"]["PROCNT_KCAL"]["quantity"]
            Update_foodlist.total_carbs = response_data["totalNutrientsKCal"]["CHOCDF_KCAL"]["quantity"]
            if (Update_foodlist.total_calories == 0):
                messages.add_message(request , messages.SUCCESS , "There is a mistake in the name")
                return render(request , 'foodlist/foodlist_form.html' , {'form' : form})
            else:
                Update_foodlist.save()
                messages.add_message(request , messages.SUCCESS , "Meal has been updated")
                return redirect(f'/foodlist/{today}')
    
    update_foodlist= FoodList.objects.get(pk=pk)
    form = FoodListForm(instance=update_foodlist)
    return render(request , 'foodlist/foodlist_form.html' , {'form' : form})

@login_required()
def delete_foodlist(request , pk):
    today = datetime.date.today()
    foodlist = FoodList.objects.get(pk=pk)
    foodlist.delete()
    messages.add_message(request , messages.SUCCESS , "Meal has been successfullly deleted!")
    return redirect(f'/foodlist/{today}')

# ----------- Comment & Like ----------- 
@login_required()
def deletecomment(request,id):
    comment=Comment.objects.get(id=id)
    comment.delete()
    return redirect('/recipe')

@login_required()
def Recipelike(request):
    if request.method == 'POST':
        post=Recipe.objects.get(id=request.POST.get('post_id'))
        is_liked=False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked=False
        else:
            post.likes.add(request.user)
            is_liked=True

        return redirect('/recipe')


# 8dd6ffa9 -> Application id
# 2684fc8a5202887d5c7167103b71f982 -> Application Keys
#  2684fc8a5202887d5c7167103b71f982	—



def search_recip(request):
    if request.method =="POST":
        searched =request.POST['searched']
        respi=Recipe.objects.filter(title__contains=searched)
        return render(request , 'recipe/search.html' ,{'searched':searched , 'respi':respi})

    else:
        return render(request , 'recipe/search.html' ,{})

def user_recipe(request):
    username = request.user
    recipes = Recipe.objects.filter(author = username)
    paginator = Paginator(recipes,3)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    try:
        recipes = paginator.page(page)
    except(EmptyPage,InvalidPage):
        recipes = paginator.page(paginator.num_pages)

    return render(request , 'recipe/user_recipe.html' , {"recipes":recipes})