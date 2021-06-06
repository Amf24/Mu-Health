from django.urls import path 
from health import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
path('', views.home, name= 'home'),
path('recipe/' , views.recipes , name= "all_recipes"),
path('recipe/new/' , views.new_recipe , name='new_recipe'),
path('recipe/<pk>/' , views.show_recipe , name="show_recipe"),
path('recipe/<pk>/update' , views.update_recipe  ,name= "update_recipe"), 
path('recipe/<pk>/delete' , views.delete_recipe , name = "delete_recipe"), 
path('foodlist/new/' , views.new_foodlist , name='new_foodlist'),
path('foodlist/<date>', views.foodlist , name="all_foodlist"),
path('foodlist/<pk>/update' , views.update_foodlist  ,name= "update_foodlist"), 
path('foodlist/<int:pk>/delete' , views.delete_foodlist , name = "delete_foodlist") , 
path('comment/<int:id>', views.deletecomment, name='health-comment'),
path('likes/',views.Recipelike,name='health-like'),
path('search/',views.search_recip,name='search_recip'),
path("user_recipe/", views.user_recipe, name="user_recipe"),

]+ static(settings.MEDIA_URL , document_root= settings.MEDIA_ROOT)
