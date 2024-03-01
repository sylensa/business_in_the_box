from django.contrib import admin

from .models import *
# Register your models here.


admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(Vendors)
admin.site.register(Category)
admin.site.register(VendorServices)
admin.site.register(Services)
admin.site.register(WishList)
admin.site.register(ReviewVendoreServices)
