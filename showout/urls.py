from django.urls import path
from . import views


#contains all paths to the various page in the application

urlpatterns = [
    #leave as empty string for base url
    path('', views.home, name = "home"),

    path('cart/', views.cart, name= "cart"),

    path('login/', views.login, name= "login"),
    
    path('signup/', views.signup, name= "signup"),

    # the rest of the path comes here

]