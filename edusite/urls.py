"""
URL configuration for edusite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from home import views as home_views
from product import views as product_views
from user import views as user_views
from balebot import views as balebot_views

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),
    path('product/<slug:slug>/', product_views.product, name='product'),
    path('pay/<slug:slug>/', product_views.pay, name='pay'),

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
    ##-----------  teacher  ---------------##
    path('add_cardbycard/', product_views.add_cardbycard, name='add_cardbycard'),

    ##-----------  teacher  ---------------##
    ##-----------  balebot  ---------------##
    path('balebot_getupdates/', balebot_views.get_updates, name='get_updates'),
    ##-----------  balebot  ---------------##




]
if settings.DEBUG:  # فقط در حالت توسعه (development)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)