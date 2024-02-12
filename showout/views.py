from django.shortcuts import render

# Create your views here.


def login(request):
    context = {}
    return render(request, 'showout/customers/login.html', context)

def signup(request):
    context = {}
    return render(request, 'showout/customers/signup.html', context)

def home(request):
    context = {}
    return render(request,'showout/customers/home.html', context)

def cart(request):
    context ={}
    return render (request, 'showout/customers/cart.html', context)

def checkout(request):
    context ={}
    return render (request, 'showout/customers/checkout.html', context)


def orderDetails(request):
    context ={}
    return render (request, 'showout/customers/orderDetails.html', context)

def orders(request):
    context ={}
    return render (request, 'showout/customers/orders.html', context)

def productDetails(request):
    context = {}
    return render (request, 'showout/customers/productDetails.html', context)

def profile(request):
    context = {}
    return render (request, 'showout/customers/profile.html', context)

def resetPassword(request):
    context = {}
    return render (request, 'showout/customers/resetPassword.html', context)

def register(request):
    context = {}
    return render (request, 'showout/customers/register.html', context)

def changePassword(request):
    context = {}
    return render (request, 'showout/customers/changePassword.html', context)

def vendorPage(request):
    context = {}
    return render (request, 'showout/customers/vendorPage.html', context)

def servicePage(request):
    context = {}
    return render (request, 'showout/customers/servicePage.html', context)

def viewServices(request):
    context = {}
    return render (request, 'showout/customers/viewServices.html', context)

def viewVendors(request):
    context = {}
    return render (request, 'showout/customers/viewVendors.html', context)

def wishlist(request):
    context = {}
    return render (request, 'showout/customers/wishlist.html', context)

def editProfile(request):
    context = {}
    return render (request, 'showout/customers/editProfile.html', context)

def aboutUS(request):
    context = {}
    return render (request, 'showout/customers/aboutUS.html', context)

def contactUS(request):
    context = {}
    return render (request, 'showout/customers/contactUS.html', context)

def searchResult(request):
    context = {}
    return render (request, 'showout/customers/searchResult.html', context)






# add the rest of the view for the various webpages