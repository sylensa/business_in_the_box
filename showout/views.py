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



# add the rest of the view for the various webpages