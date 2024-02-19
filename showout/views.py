from django.shortcuts import render, redirect
from .forms import VendorRegistrationForm, CustomerRegistrationForm
from .models import *
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Vendors, Customer
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.

def is_user_logged_in(request):
    return 'user_id' in request.session

def my_logout_view(request):
    del request.session['user_id']  # Remove user ID from session
    # Redirect to a logout success page or any other desired page
    return redirect('home')

def customerLogin(request): 
    if 'user_id' in request.session:
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
        categories = Category.objects.all()
        vendorServices = VendorServices.objects.all()
        vendors = Vendors.objects.all()
        context = {'categories':categories,'vendorServices':vendorServices,'vendors':vendors,'customer':customer}
        return redirect('home')  
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate_customer(email, password)
            if user is not None:
                # Authentication successful, perform login manually
                request.session['user_id'] = user.customerId  # Store user ID in session
                # Redirect to a success page or home page
                return redirect('home')
            else:
                # Authentication failed, display error message
                messages.error(request, 'Invalid email or password')
        return render(request, 'showout/customers/login.html')


def signup(request):

    context = {}
    return render(request, 'showout/customers/signup.html', context)

def home(request):  
    categories = Category.objects.all()
    vendorServices = VendorServices.objects.all()
    vendors = Vendors.objects.all()
    user = None
    if 'user_id' in request.session:
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
    else:
        customer = None
    context = {'categories':categories,'vendorServices':vendorServices,'vendors':vendors,'customer':customer}
    return render(request,'showout/customers/home.html', context)
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
    if request.method == 'POST':
        # Retrieve registration data from POST request
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        mobile = request.POST['mobile']
        confirm_password = request.POST['confirm_password']
        password = request.POST['password']
        # Create a new Client instance and save it to the database
        user = Customer.objects.create(firstName=fname, email=email, password=password, lastName=lname, mobile=mobile)

        # Log in the newly registered user
        login(request, user)

        # Redirect to a success page or client dashboard
        return redirect('home')
    else:
        return render(request, 'showout/customers/register.html')


def changePassword(request):
    context = {}
    return render (request, 'showout/customers/changePassword.html', context)

def vendorPage(request,vendorId):
    vendorServices = VendorServices.objects.all()
    vendorServices = getVendorsServices(vendorServices,vendorId)
    categories = Category.objects.all()
    context = {'vendorServices':vendorServices,'vendor':vendorServices[0].vendor,'categories':categories}
    return render (request, 'showout/customers/vendorPage.html', context)

def servicePage(request,vendorId,serviceId):
    print("vendorId",  vendorId)
    print("serviceId",  serviceId)
    vendorServices = [];
    vendorServices = VendorServices.objects.all()
    categories = Category.objects.all()
    vendorService = getVendorService(vendorServices,serviceId,vendorId)
    vendorSimilarServices = getVendorSimilarService(vendorServices,serviceId)
    context = {'vendorService':vendorService,'vendorSimilarServices':vendorSimilarServices,'categories':categories}
    return render (request, 'showout/customers/servicePage.html', context)

def viewServices(request,categoryId,categoryName):
    vendorServices = VendorServices.objects.all()
    categories = Category.objects.all()
    servicesByCategory = getVendorsByCategory(vendorServices,categoryId)
    context = {'servicesByCategory':servicesByCategory,'categoryName':categoryName,'categories':categories}
    return render (request, 'showout/customers/viewServices.html', context)

def viewVendors(request):
    vendors = Vendors.objects.all()
    categories = Category.objects.all()
    context = {'vendors':vendors,'categories':categories}
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
    categories = Category.objects.all()
    if request.method == 'POST':
       query = request.POST.get('query')
    # Perform search or other processing with the query
       searchResultsServices = fetchSearchResults(query);
       context = {'searchResultsServices':searchResultsServices,'categories':categories}
    #    return HttpResponse(f'Searching for: {query}')

    return render (request, 'showout/customers/searchResult.html', context)


# vendor views



def customerlist(request):
    context = {}
    return render (request, 'showout/vendor/customerlist.html', context)
def vendor_dash(request):
    context = {}
    return render (request, 'showout/vendor/vendor_dash.html', context)


def document(request):
    context = {}
    return render (request, 'showout/vendor/document.html', context)


def getVendorService(vendorServices,serviceId,vendorId):
   for vendorService in vendorServices:
        if vendorService.services.serviceId == serviceId and vendorService.vendor.vendorId == vendorId:
            return vendorService
            break


def getVendorSimilarService(vendorServices,serviceId):
   vendorSimilarServices = [];
   for vendorService in vendorServices:
        if vendorService.services.serviceId == serviceId :
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices


def getVendorsServices(vendorServices,vendorId):
   vendorSimilarServices = [];
   for vendorService in vendorServices:
        if vendorService.vendor.vendorId == vendorId:
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices

def getVendorsByCategory(vendorServices,categoryId):
   vendorSimilarServices = [];
   for vendorService in vendorServices:
        if vendorService.category.categoryId == categoryId:
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices


def fetchSearchResults(userSearch):
    services = []
    categories = Category.objects.filter(categoryName__icontains=userSearch)
    vendors = Vendors.objects.filter(vendorName__icontains=userSearch)
    vendorServices = VendorServices.objects.all()
    for category in categories:
        for vendorService in vendorServices:
            if category.categoryId == vendorService.category.categoryId:
                services.append(vendorService)

    for vendor in vendors:
        for vendorService in vendorServices:
            if vendor.vendorId == vendorService.vendor.vendorId:
                services.append(vendorService)
 

    return services

def authenticate_customer(email, password):
    try:
        customer = Customer.objects.get(email=email)
        if customer.password == password:
            return customer
    except Customer.DoesNotExist:
        return None