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






# add the rest of the view for the various webpages