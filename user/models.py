from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from health.models import Recipe , FoodList 

gender_choice = (
    ('male'  , 'male'),
    ('female' , 'female')
    )

goal_choices = (
    ('lose weight','lose wight'),
    ('gain weight', 'gain weight')
)

activity_choices = (
    ('not active','not active'),
    ('somewhat active','somewhat active'),
    ('medium active','medium active'),
    ('highly active','highly active'),
    ('extremely active','extremely active')
)
 
class Profile(models.Model):
    user = models.OneToOneField(User , related_name = "profile",null=True, on_delete=models.CASCADE)
    bmi = models.FloatField(null=True)
    goal_weight = models.FloatField(null=True)
    # Favorite 
    calorites_total = models.FloatField(null=True)
    # Add user's recipies 
    # foodlist = models.ForeignKey(FoodList , related_name = 'foodlist', on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(choices = gender_choice , null=True , max_length=255)
    height = models.PositiveIntegerField(null=True)
    goal_type = models.CharField(null=True, choices=goal_choices, max_length=255)
    activity_level = models.CharField(null=True, choices=activity_choices, max_length=255)
    weight = models.FloatField(null=True)
    image = models.ImageField(upload_to ="img/" , null=True)


    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance , created, **kwargs):
    if created:
        Profile.objects.create(user=instance, id=instance.id)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
