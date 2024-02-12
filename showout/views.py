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


def vendor_list(request):
    context ={}
    return render (request, 'showout/vendor_list.html', context)

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


def dashboard(request):
    context = {}
    return render (request, 'showout/dashboard.html', context)






# add the rest of the view for the various webpages