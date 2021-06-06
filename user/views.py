from django.shortcuts import render , redirect ,HttpResponseRedirect
from .forms import UserForm , ProfileForm
from django.contrib import messages
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import FoodList , Recipe
from . import forms
from datetime import date


# Create your views here.


def register(request):
    form = UserForm()
    form_profile = ProfileForm()

    if (request.method == "POST"):
        user = UserForm(request.POST)
        if (user.is_valid()):
            user = user.save(commit = True)
            profile = ProfileForm(request.POST ,request.FILES, instance= user.profile)
            if (profile.is_valid()):
                print("SUCCESS")
                profile.save()
                messages.add_message(request , messages.SUCCESS , "Welcome to Mu Health")
                return redirect('home')
        else:
            form = user

    return render(request , 'register.html' , {"form" : form , "ProfileForm":ProfileForm})


def profile(request):
    # foods = FoodList.objects.filter(date = date.today())
    foods = FoodList.objects.filter(date=date.today())
    username = request.user
    print(foods)
    recipes = Recipe.objects.filter(author = username)
    today = date.today()

    paginator = Paginator(recipes,1)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    try:
        recipes = paginator.page(page)
    except(EmptyPage,InvalidPage):
        recipes = paginator.page(paginator.num_pages)
    

    return render(request , 'profile.html' , {"foods" : foods , "recipes":recipes , "today":today})


# def edit_user_profile(request):
#     """Edit user profile information."""
#     user = request.user
#     form1 = forms.UserUpdateForm(instance=user)
#     form2 = forms.ProfileForm(instance=user.profile)
#     if request.method == 'POST':
#         form1 = forms.UserUpdateForm(instance=user, data=request.POST)
#         form2 = forms.ProfileForm(
#             instance=user.profile,
#             data=request.POST,
#             files=request.FILES
#         )
#         if form1.is_valid() and form2.is_valid():
#             form1.save()
#             form2.save()
#             messages.success(request, "Your profile has been updated!")
#             return HttpResponseRedirect('profile')
#     return render(request, 'edit_profile.html',
#         {'form1': form1, 'form2': form2})

def edit_user_profile(request):
    user = request.user
    form = forms.UserUpdateForm(instance=user)
    form_profile = ProfileForm(instance=user.profile)
    if (request.method == "POST"):
        user = forms.UserUpdateForm(instance=user, data=request.POST)
        if (user.is_valid()):
            user = user.save(commit = True)
            profile = ProfileForm(request.POST , request.FILES,instance= user.profile)
            if (profile.is_valid()):
                profile.save()
                messages.add_message(request , messages.SUCCESS , "Your profile Has Been Updated Successfully")
                return redirect('profile')
        else:
            form = user

    return render(request , 'edit_profile.html' , {"form" : form , "ProfileForm":form_profile})

def delete_view(request):
	if request.method == "POST":
		username = request.user.username
		user = User.objects.get(username=username)
		user.delete()
		messages.error(request, f"{user.username}'s account has been deleted.")
		return redirect("register")
	return render(request, 'delete.html')

