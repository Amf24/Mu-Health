from django.forms import ModelForm
from .models import Profile
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ( 'username', 'first_name' , "last_name" , "email" , )

class ProfileForm(ModelForm): 
    class Meta:
        model = Profile
        fields = ( "image","age","gender","height","weight","goal_type","activity_level")
class UserUpdateForm(forms.ModelForm):
      class Meta: 
        model = User
        fields = ( 'username', 'first_name' , "last_name" , "email" , )
# class UpdateProfileForm(forms.ModelForm): 
#     class Meta:
#         model = Profile
#         fields = ("age","gender","height","weight","goal_type","activity_level")