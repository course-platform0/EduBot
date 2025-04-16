
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from user import views


urlpatterns = [

    ##-----------  user  ---------------##
    path('register/', user_views.register, name='register'),
    path('verify/', user_views.verify, name='verify'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('forgetpassword/', user_views.forget_password, name='forget_password'),
    path('verifyforgetpassword/', user_views.verify_forget_password, name='verify_forget_password'),
    path('profile/', user_views.profile, name='profile'),
    path('testsms/', user_views.testsms, name='testsms'),
    ##-----------  user  ---------------##



]
