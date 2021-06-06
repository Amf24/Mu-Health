from django.urls import path 
from django.contrib.auth import views as as_view
from django.contrib.auth import views as auth_views
from user import views

urlpatterns = [
    path('login/' , as_view.LoginView.as_view(template_name = "login.html") , name= "login"),
    path('logout/' , as_view.LogoutView.as_view() , name= "logout") , 
    path('register/' ,views.register , name="register" ),
    path('profile/' , views.profile , name="profile" ),
    path('profile/edit' , views.edit_user_profile , name="editprofile" ),
    path("delete/", views.delete_view, name="delete"),



    # path('register_info/' ,views.register_info , name="register_info" ) edit_user_profile,
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset/password_reset_sent.html"), name="password_reset_done"),
    path('reset_/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="reset/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset/password_reset_done.html"), name="password_reset_complete"),
]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''