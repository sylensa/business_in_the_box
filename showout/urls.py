from django.urls import path
from . import views


#contains all paths to the various page in the application

urlpatterns = [
    #leave as empty string for base url
    path('', views.home, name = "home"),

    path('cart/', views.cart, name= "cart"),

    path('checkout/', views.checkout, name= "checkout"),

    path('login/', views.login, name= "login"),
    
    path('signup/', views.signup, name= "signup"),

    path('orderDetails/', views.orderDetails, name="order_details"),

    path ('orders/', views.orders, name="orders"),

    path ('productDetails/', views.productDetails, name="product_details"),

    path ('profile/', views.profile, name="profile"),

    path ('resetPassword/', views.resetPassword, name="reset_password"),

    



    # the rest of the path comes here

]