from django.forms import ModelForm
from django import forms

from .models import FoodList , Recipe  , Comment

class FoodListForm(ModelForm):

    class Meta:
        model = FoodList
        fields = ("date","meal_type","meal_name","quantity")


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ("title","text","calories","image","date")



class CommentForm(forms.ModelForm):
    content = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Leave a review here ...',
        'rows':2,
        'cols':80
    }))
    class Meta:
        model = Comment
        fields =['content']
