from django.shortcuts import render

# Create your views here.


def login(request):
    context = {}
    return render(request, 'showout/login.html', context)

def signup(request):
    context = {}
    return render(request, 'showout/signup.html', context)

def home(request):
    context = {}
    return render(request,'showout/home.html', context)

def cart(request):
    context ={}
    return render (request, 'showout/cart.html', context)

def checkout(request):
    context ={}
    return render (request, 'showout/checkout.html', context)


def orderDetails(request):
    context ={}
    return render (request, 'showout/orderDetails.html', context)

def orders(request):
    context ={}
    return render (request, 'showout/orders.html', context)

def productDetails(request):
    context = {}
    return render (request, 'showout/productDetails.html', context)

def profile(request):
    context = {}
    return render (request, 'showout/profile.html', context)


    context = {}
    return render (request, 'showout/report.html', context)
def resetPassword(request):
    context = {}
    return render (request, 'showout/resetPassword.html', context)

def register(request):
    context = {}
    return render (request, 'showout/register.html', context)

def changePassword(request):
    context = {}
    return render (request, 'showout/changePassword.html', context)

def vendorPage(request):
    context = {}
    return render (request, 'showout/vendorPage.html', context)

def servicePage(request):
    context = {}
    return render (request, 'showout/servicePage.html', context)

def viewServices(request):
    context = {}
    return render (request, 'showout/viewServices.html', context)

def viewVendors(request):
    context = {}
    return render (request, 'showout/viewVendors.html', context)

def wishlist(request):
    context = {}
    return render (request, 'showout/wishlist.html', context)

def editProfile(request):
    context = {}
    return render (request, 'showout/editProfile.html', context)

def aboutUS(request):
    context = {}
    return render (request, 'showout/aboutUS.html', context)

def contactUS(request):
    context = {}
    return render (request, 'showout/contactUS.html', context)

def searchResult(request):
    context = {}
    return render (request, 'showout/searchResult.html', context)






# add the rest of the view for the various webpages