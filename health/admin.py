from django.contrib import admin
from .models import Recipe , FoodList , Comment
# Register your models here.

admin.site.register(Recipe)
admin.site.register(FoodList)
admin.site.register(Comment) 



