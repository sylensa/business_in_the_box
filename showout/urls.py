from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

#contains all paths to the various page in the application

urlpatterns = [
    #leave as empty string for base url
    path('', views.home, name = "home"),



    #customer urls
    path('customerLogin/', views.customerLogin, name= "customerLogin"),
     path ('customer_settings/', views.customer_settings, name="customer_settings"),
    path('signup/', views.signup, name= "signup"),
    path('logout/', views.my_logout_view, name='logout'),
     path('vendorLogout/', views.vendor_logout_view, name='vendorLogout'),
     path ('profile/', views.profile, name="profile"),
    path('update_item/', views.updateItem, name="update_item"),
    path('update_rating/', views.updateRating, name="update_rating"),
    
    path ('resetPassword/', views.resetPassword, name="reset_password"),
     path ('sendEmail/', views.sendEmail, name="sendEmail"),
      path ('changePassword/', views.changePassword, name="changePassword"),
        path ('vendorWishlist/', views.vendorWishlist, name="vendorWishlist"),
         path ('vendorServices/', views.vendorServices, name="vendorServices"),
     
     path ('emailSent/', views.emailSent, name="emailSent"),

    path ('register/', views.register, name="register"),

    path ('changePassword/', views.register, name="change_password"),

    path ('vendorPage/<int:vendorId>', views.vendorPage, name="vendorPage"),

    path ('servicePage/<int:vendorId>/<int:serviceId>', views.servicePage, name="servicePage"),

    path ('viewServices/<int:categoryId>/<str:categoryName>', views.viewServices, name="viewServices"),

    path ('viewVendors/', views.viewVendors, name="viewVendors"),

    path ('wishlist/', views.wishlist, name="wishlist"),
     path ('wishlistHistory/', views.wishlistHistory, name="wishlistHistory"),
     path ('topRatedServices/', views.topRatedServices, name="topRatedServices"),

    path ('editProfile/', views.editProfile, name="editProfile"),

    path ('aboutUS/', views.aboutUS, name="aboutUS"),

    path ('contactUS/', views.contactUS, name="contactUS"),

    path ('searchResult/', views.searchResult, name="searchResult"),
   
    
    



    # vendor urls
    path ('vendor_login/', views.vendor_login, name="vendor_login"),
    path ('vendor_sign_up/', views.vendor_sign_up, name="vendor_sign_up"),
    path ('vendor_password_reset/', views.vendor_password_reset, name="vendor_password_reset"),
    path ('vendor_change_password/', views.vendor_change_password, name="vendor_change_password"),
    
    path ('vendor_dash/', views.vendor_dash, name="vendor_dash"),
    path ('customerlist/', views.customerlist, name="customerlist"),
    path ('document/', views.document, name="document"),
    path ('vendor_settings/', views.vendor_settings, name="vendor_settings"),
    path ('add_service/', views.add_service, name="add_service"),
   
    
   
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)