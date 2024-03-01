from django.urls import path,include
from . import views

#contains all paths to the various page in the application

urlpatterns = [
    #leave as empty string for base url
    path('', views.home, name = "home"),



    #customer urls
    path('customerLogin/', views.customerLogin, name= "customerLogin"),
    
    path('signup/', views.signup, name= "signup"),
    path('logout/', views.my_logout_view, name='logout'),
     path ('profile/', views.profile, name="profile"),
    path('update_item/', views.updateItem, name="update_item"),
    path('update_rating/', views.updateRating, name="update_rating"),
    
    path ('resetPassword/', views.resetPassword, name="reset_password"),

    path ('register/', views.register, name="register"),

    path ('changePassword/', views.register, name="change_password"),

    path ('vendorPage/<int:vendorId>', views.vendorPage, name="vendorPage"),

    path ('servicePage/<int:vendorId>/<int:serviceId>', views.servicePage, name="servicePage"),

    path ('viewServices/<int:categoryId>/<str:categoryName>', views.viewServices, name="viewServices"),

    path ('viewVendors/', views.viewVendors, name="viewVendors"),

    path ('wishlist/', views.wishlist, name="wishlist"),
     path ('wishlistHistory/', views.wishlistHistory, name="wishlistHistory"),

    path ('editProfile/', views.editProfile, name="editProfile"),

    path ('aboutUS/', views.aboutUS, name="aboutUS"),

    path ('contactUS/', views.contactUS, name="contactUS"),

    path ('searchResult/', views.searchResult, name="searchResult"),

    
    



    # vendor urls
   
    path ('customerlist/', views.customerlist, name="customerlist"),
    path ('vendor_dash/', views.vendor_dash, name="vendor_dash"),
    path ('document/', views.document, name="document"),
    path ('vendor_login/', views.vendor_login, name="vendor_login"),
    path ('vendor_sign_up/', views.vendor_sign_up, name="vendor_sign_up"),

]
