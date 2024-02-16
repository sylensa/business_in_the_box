from django.urls import path
from . import views


#contains all paths to the various page in the application

urlpatterns = [
    #leave as empty string for base url
    path('', views.home, name = "home"),



    #customer urls
    path('login/', views.login, name= "login"),
    
    path('signup/', views.signup, name= "signup"),

     path ('profile/', views.profile, name="profile"),

    path ('resetPassword/', views.resetPassword, name="reset_password"),

    path ('register/', views.register, name="register"),

    path ('changePassword/', views.register, name="change_password"),

    path ('vendorPage/', views.vendorPage, name="vendorPage"),

    path ('servicePage/', views.servicePage, name="servicePage"),

    path ('viewServices/', views.viewServices, name="viewServices"),

    path ('viewVendors/', views.viewVendors, name="viewVendors"),

    path ('customers/wishlist/', views.wishlist, name="wishlist"),

    path ('editProfile/', views.editProfile, name="editProfile"),

    path ('aboutUS/', views.aboutUS, name="aboutUS"),

    path ('contactUS/', views.contactUS, name="contactUS"),

    path ('searchResult/', views.searchResult, name="searchResult"),

    
    



    # vendor urls
   
    path ('customerlist/', views.customerlist, name="customerlist"),
    path ('vendor_dash/', views.vendor_dash, name="vendor_dash"),
    
    
]
