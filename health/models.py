from django.db import models
from datetime import datetime
from user.models import User
# Create your models here.

meal_choices = (
    ('breakfest'  , 'breakfest'),
    ('lunch' , 'lunch'),
    ('dinner','dinner')
)


class Recipe(models.Model):
    title = models.CharField(max_length= 50, null=True)
    text = models.TextField(null=True)
    calories = models.FloatField(null=True)
    image =  models.ImageField(upload_to ="img/" , null=True)
    date = models.DateField(null=True, default = datetime.now)
    author = models.ForeignKey(User , related_name = "author" , on_delete=models.CASCADE, null = True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)

    # Add comment

    def __str__(self):
        return self.title 
    def likecount(self):
    	return self.likes.count()

class FoodList(models.Model):
    date = models.DateField(null=True, default = datetime.now)
    meal_type = models.CharField(null=True , choices=meal_choices , max_length=255) # user.foodlist | filter.meal_type="lunch"
    meal_name = models.CharField(null=True, max_length=50)
    total_calories = models.FloatField(null=True)
    total_fat = models.FloatField(null=True)
    total_protein = models.FloatField(null=True)
    total_carbs = models.FloatField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(User , related_name = "foodlist" , on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.meal_name

class Comment(models.Model):
	post=models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='comments' ,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE ,null=True)
	content=models.TextField(null=True)
	timestamp=models.DateTimeField(auto_now_add=True ,null=True)

	def __str__(self):
		return 'comment on {} by {}'.format(self.post.title,self.user.username)

