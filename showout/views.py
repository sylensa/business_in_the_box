# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from django.shortcuts import render, redirect
from .forms import VendorRegistrationForm, CustomerRegistrationForm
from .models import *
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Vendors, Customer
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
import json
from django.db.models import Count,Avg
from .models import Image
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Create your views here.
emailToken = "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"

def is_user_logged_in(request):
    return 'user_id' in request.session

def my_logout_view(request):
    
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user ID from session
    if 'cart' in request.session:    
        del request.session['cart'] 
    # Redirect to a logout success page or any other desired page
    return redirect('home')

def sendEmail(request):
    if request.method == 'POST':
        subject = 'Hello from Django'
        to_email =  request.POST['email']  # Replace with the recipient's email address
        context = {'link': f'http://127.0.0.1:8000/changePassword/?email={to_email}'}
        template_path = 'showout/customers/email_template.html'
        messageString = render_to_string(template_path, context)
        from_email = 'hello@showout.studio'  # Replace with your email address
        print("to_email",to_email)    
        message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=messageString)
        try:
            sg = SendGridAPIClient(emailToken)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return redirect('emailSent')

        except Exception as e:
            print(e)
        return redirect('reset_password')   

def sendVendorEmail(request):
    if request.method == 'POST':
        subject = 'Hello from Django'
        to_email =  request.POST['email']  # Replace with the recipient's email address
        context = {'link': f'http://127.0.0.1:8000/vendor_change_password/?email={to_email}'}
        template_path = 'showout/customers/email_template.html'
        messageString = render_to_string(template_path, context)
        from_email = 'hello@showout.studio'  # Replace with your email address
        print("to_email",to_email)    
        message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=messageString)
        try:
            sg = SendGridAPIClient(emailToken)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return redirect('emailSent')

        except Exception as e:
            print(e)
        return redirect('vendor_password_reset')   


def emailSent(request):
   return render(request, 'showout/customers/email_sent.html')

def vendor_logout_view(request):
    if 'vendor_id' in request.session:
        del request.session['vendor_id']  # Remove user ID from session
    # Redirect to a logout success page or any other desired page
    return redirect('vendor_login')

def updateItem(request):
    request.session.modified = True

    data = json.loads(request.body)
    vendorServicesId = data['vendorServicesId']
    vendorService = VendorServices.objects.get(vendorServicesId=vendorServicesId)
    action = data['action']
    print('Action:', action)
    print('vendorService:', vendorService)
    cart = request.session.get('cart', {})
    cart_item = cart.get(vendorService.vendorServicesId, {'quantity': 0})
    if action == 'add':
      cart_item['quantity'] += 1
    elif action == 'remove':
      cart_item['quantity'] -= 1
    cart[vendorService.vendorServicesId] = cart_item
    request.session['cart'] = cart
    if cart_item['quantity'] <= 0 :
        del  request.session['cart'][vendorService.vendorServicesId] 
        del  request.session['cart'][str(vendorService.vendorServicesId)]
        print("ccart",request.session['cart'])

    return JsonResponse('Item was added', safe=False)

def updateRating(request):
    if 'user_id' in request.session:
        data = json.loads(request.body)
        ratingValue = data['ratingValue']
        vendorServicesId = data['vendorServicesId']
        customerId = request.session['user_id']
        review = data['review']
        vendorService = VendorServices.objects.get(vendorServicesId=vendorServicesId)
        customer = Customer.objects.get(customerId=customerId)
        print("ratingValue",ratingValue)
        print("vendorServicesId",vendorServicesId)
        print("customerId",customerId)
        print("review",review)

        reviewVendoreServices = ReviewVendoreServices.objects.create(vendorService=vendorService, customer=customer, rating=ratingValue, review=review,vendorServicesId=vendorServicesId,vendor=vendorService.vendor)

   
    return JsonResponse('Service rated succcessfully', safe=False)

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
    listVendorServices = appRatingToService(vendorServices)
    vendors = Vendors.objects.all()
    listVendors = appRatingToVendors(vendors)
    user = None
    if 'user_id' in request.session:
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
    else:
        customer = None
    context = {'categories':categories,'vendorServices':listVendorServices,'vendors':listVendors,'customer':customer}
   
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
    countries = Country.objects.all(); 
    genders = Gender.objects.all(); 
    if request.method == 'POST':
        # Retrieve registration data from POST request
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        mobile = request.POST['mobile']
        genderId = request.POST['genderId']
        countryId = request.POST['countryId']
        confirm_password = request.POST['confirm_password']
        password = request.POST['password']
        address = request.POST['address']
        
        # Create a new Client instance and save it to the database
        Customer.objects.create(firstName=fname, email=email, password=password, lastName=lname, mobile=mobile,genderId=genderId,countryId=countryId,address=address)
        user = authenticate_customer(email, password)
        if user is not None:
            # Authentication successful, perform login manually
            request.session['user_id'] = user.customerId  # Store user ID in session
            # Redirect to a success page or home page
            return redirect('home')
        else:
            # Authentication failed, display error message
            messages.error(request, 'Invalid email or password')

    else:
        return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})

def changePassword(request):
   password = ''
   confirmPassword = ''
   email = ''
   if request.method == 'GET':
    email =  request.GET['email']
    request.session['customerEmail']  = email;
    return render(request,'showout/customers/changePassword.html')  
   if request.method == 'POST': 
        password =  request.POST['password']
        confirmPassword =  request.POST['confirm_password']

        email = request.session['customerEmail'] 
        customer = Customer.objects.get(email=email)
        customer.password = password
        customer.save()
        print("email",email)
        print("password",password)
        print("confirmPassword",confirmPassword)
        if 'user_id' in request.session:
          del request.session['user_id'] 
        context = {}
        return redirect('customerLogin')  

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
    average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
    if average_rating:
       vendorService.rating = average_rating["rating"]
    print("average_rating",average_rating)
    reviewVendoreServices = ReviewVendoreServices.objects.filter(vendorService=vendorService)
    context = {'vendorService':vendorService,'vendorSimilarServices':vendorSimilarServices,'categories':categories,'reviewVendoreServices':reviewVendoreServices}
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
    carts =  request.session['cart'] 
    listVendorServices = []
    vendorServices = VendorServices.objects.all()
    for cart in carts:
        for vendorService in vendorServices:
            if vendorService.vendorServicesId == int(cart):
                     average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                     if average_rating:
                        vendorService.rating = average_rating["rating"]
                     listVendorServices.append(vendorService)
    context = {'vendorServices':listVendorServices}
    if request.method == 'POST' and  'user_id' in request.session: 
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
        for vendorService in listVendorServices:
         wishList = WishList.objects.create(vendorService=vendorService, customer=customer, vendor=vendorService.vendor)

        wishlistServices =  WishList.objects.filter(customer=customer)
        listWishlistServices  = getWishListVendorService(wishlistServices)


        return render (request, 'showout/customers/wishlistHistory.html', {'wishlistServices':listWishlistServices})

    else:
        return render (request, 'showout/customers/wishlist.html', context)

def wishlistHistory(request):
    wishlistServices = []
    if 'user_id' in request.session: 
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
        wishlistServices =  WishList.objects.filter(customer=customer)
        listWishlistServices  = getWishListVendorService(wishlistServices)

    return render (request, 'showout/customers/wishlistHistory.html', {'wishlistServices':listWishlistServices})
    
def topRatedServices(request):
    mostReviewedServices = []
    reviews_grouped = ReviewVendoreServices.objects.values('vendorService').annotate(rating=Avg('rating'))
    most_reviewed_services = [  
    ReviewVendoreServices.objects.filter(vendorService=item['vendorService']).first()
    for item in reviews_grouped
        ]
    for most_reviewed_service in most_reviewed_services:
        average_rating = ReviewVendoreServices.objects.filter(vendorService=most_reviewed_service.vendorService).aggregate(rating=Avg('rating'))
        if average_rating:
            most_reviewed_service.vendorService.rating = average_rating["rating"]
            mostReviewedServices.append(most_reviewed_service)
    print("mostReviewedServices",most_reviewed_services)
    return render (request, 'showout/customers/topRatedServices.html', {'mostReviewedServices':mostReviewedServices})
    
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


def customer_settings(request):
    countries = Country.objects.all()
    genders = Gender.objects.all()
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        customer = Customer.objects.get(pk=user_id)
        context = {'countries':countries,'customer':customer,'genders':genders}
        if request.method == 'POST':
            # Retrieve registration data from POST request
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            mobile = request.POST['mobile']
            genderId = request.POST['genderId']
            countryId = request.POST['countryId']
            address = request.POST['address']
            customer.email = email
            customer.firstName = fname
            customer.lastName = lname
            customer.countryId = countryId
            customer.address = address
            customer.mobile = mobile
            customer.genderId = genderId
            customer.save()
            print("fname",fname)
            print("genderId",genderId)
            print("countryId",countryId)
            print("email",email)
            print("lname",lname)
            return redirect('customer_settings')        
        else:
            
            return render (request, 'showout/customers/customer_settings.html', context) 
    else:
         return redirect('login')



# vendor views

def vendor_login(request):
    if 'vendor_id' in request.session:
        print("hello1")
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        categories = Category.objects.all()
        vendorServices = VendorServices.objects.all()
        vendors = Vendors.objects.all()
        # context = {'categories':categories,'vendorServices':vendorServices,'vendors':vendors,'customer':customer}
       
        return redirect('vendor_dash')  
    else:
       
        if request.method == 'POST':
            print("hello")
            email = request.POST['email']
            password = request.POST['password']
            vendor = authenticate_vendor(email, password)
            if vendor is not None:
                # Authentication successful, perform login manually
                request.session['vendor_id'] = vendor.vendorId  # Store user ID in session
                # Redirect to a success page or home page
                return redirect('vendor_dash')
            else:
                # Authentication failed, display error message
                print('Invalid email or password')
                messages.error(request, 'Invalid email or password')
        return render(request, 'showout/vendor/vendor_login.html')

def vendor_sign_up(request):
    if request.method == 'POST':
        # Retrieve registration data from POST request
        email = request.POST['email']
        vendorName = request.POST['vendorName']
        mobile = request.POST['mobile']
        countryId = request.POST['countryId']
        address = request.POST['address']
        confirm_password = request.POST['confirm_password']
        password = request.POST['password']
        image = request.FILES.get('image')
        print("image:",image)
        # Create a new Client instance and save it to the database
        Vendors.objects.create(vendorName=vendorName, email=email, password=password, countryId=countryId, mobile=mobile,address=address,genderId=1,image=image)
        vendor = authenticate_vendor(email, password)
        if vendor is not None:
            # Authentication successful, perform login manually
            request.session['vendor_id'] = vendor.vendorId  # Store user ID in session
            # Redirect to a success page or home page
            return redirect('vendor_dash')
        else:
            # Authentication failed, display error message
            messages.error(request, 'Invalid email or password')
    else:
        countries = Country.objects.all()
        genders = Gender.objects.all()
        return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})

def customerlist(request):
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        wishLists = WishList.objects.filter(vendor=vendor)
        customers = wishLists.values('customer').annotate(count=Count('customer'))
        allCustomers = [  
        WishList.objects.filter(customer=item['customer']).first()
        for item in customers
            ]
        print("wishLists",allCustomers)
   
    context = {'wishLists':allCustomers}
    return render (request, 'showout/vendor/customerlist.html', context)

def vendorWishlist(request):
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        wishLists = WishList.objects.filter(vendor=vendor)
       
   
        context = {'wishLists':wishLists}
    return render (request, 'showout/vendor/vendor_wishlist.html', context)

def vendor_services(request):
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        vendorServices = VendorServices.objects.filter(vendor=vendor)
       
   
    context = {'vendorServices':vendorServices}
    return render (request, 'showout/vendor/vendor_services.html', context)

def vendor_dash(request):
    listVendorServices = []
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        print("vendor",vendor)
        print("vendorId",vendorId)
        vendorServices = VendorServices.objects.filter(vendor=vendor)
        listVendorServices = appRatingToService(vendorServices)
        wishLists = WishList.objects.filter(vendor=vendor)
        customers = wishLists.values('customer').annotate(count=Count('customer'))
        print("customers",customers)
        return render (request, 'showout/vendor/vendor_dash.html', {"vendorServices":listVendorServices, "wishLists":wishLists,"customers":customers})

    else:
        return redirect('vendor_login') 

def document(request):
    context = {}
    return render (request, 'showout/vendor/document.html', context)

def getWishListVendorService(wishlistServices):
    listWishlistService = []
    for wishlistService in wishlistServices:
            average_rating = ReviewVendoreServices.objects.filter(vendorService=wishlistService.vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                wishlistService.vendorService.rating = average_rating["rating"]
            listWishlistService.append(wishlistService)
        
    
    return listWishlistService
        
def getVendorService(vendorServices,serviceId,vendorId):
   for vendorService in vendorServices:
        if vendorService.services.serviceId == serviceId and vendorService.vendor.vendorId == vendorId:
            average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                vendorService.rating = average_rating["rating"]
            return vendorService
            break

def appRatingToService(vendorServices):
    listVendorServices = []
    for vendorService in vendorServices:
        average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
        if average_rating:
            vendorService.rating = average_rating["rating"]
        listVendorServices.append(vendorService)

    return listVendorServices

def appRatingToVendors(vendors):
    listVendors = []
    for vendor in vendors:
        average_rating = ReviewVendoreServices.objects.filter(vendor=vendor).aggregate(rating=Avg('rating'))
        if average_rating:
            vendor.rating = average_rating["rating"]
        listVendors.append(vendor)

    return listVendors

def getVendorSimilarService(vendorServices,serviceId):
   vendorSimilarServices = [];
   for vendorService in vendorServices:
        if vendorService.services.serviceId == serviceId :
            average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                vendorService.rating = average_rating["rating"]
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices

def getVendorsServices(vendorServices,vendorId):
   vendorSimilarServices = [];
   for vendorService in vendorServices:
        if vendorService.vendor.vendorId == vendorId:
            average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                vendorService.rating = average_rating["rating"]
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices

def getVendorsByCategory(vendorServices,categoryId):
   vendorSimilarServices = [];
   for vendorService in vendorServices:
        if vendorService.category.categoryId == categoryId:
            average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                vendorService.rating = average_rating["rating"]
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
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                services.append(vendorService)

    for vendor in vendors:
        for vendorService in vendorServices:
            if vendor.vendorId == vendorService.vendor.vendorId:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                services.append(vendorService)
 

    return services

def authenticate_customer(email, password):
    try:
        customer = Customer.objects.get(email=email)
        if customer.password == password:
            return customer
    except Customer.DoesNotExist:
        return None
    
def authenticate_vendor(email, password):
    try:
        vendor = Vendors.objects.get(email=email)
        if vendor.password == password:
            return vendor
    except vendor.DoesNotExist:
        return None
    

def vendor_password_reset(request):
    context = {}
    return render (request, 'showout/vendor/vendor_password_reset.html', context)

def vendor_change_password(request):
  password = ''
  confirmPassword = ''
  email = ''
  if request.method == 'GET':
    email =  request.GET['email']
    request.session['vendorEmail']  = email;
    return render(request,'showout/vendor/vendor_change_password.html')  
  if request.method == 'POST': 
        password =  request.POST['password']
        confirmPassword =  request.POST['confirm_password']
        email = request.session['vendorEmail'] 
        vendor = Vendors.objects.get(email=email)
        vendor.password = password
        vendor.save()
        print("email",email)
        print("password",password)
        print("confirmPassword",confirmPassword)
        if 'vendor_id' in request.session:
         del request.session['vendor_id']
        context = {}
        return redirect('vendor_login') 

def vendor_settings(request):
    countries = Country.objects.all()
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        context = {'countries':countries,'vendor':vendor}
        if request.method == 'POST':
            # Retrieve registration data from POST request
            email = request.POST['email']
            vendorName = request.POST['vendorName']
            mobile = request.POST['mobile']
            countryId = request.POST['countryId']
            address = request.POST['address']
            aboout = request.POST['aboout']
            website = request.POST['website']
            # image = request.FILES.get('image')
            vendor.email = email
            vendor.vendorName = vendorName
            vendor.countryId = countryId
            vendor.mobile = mobile
            vendor.address = address
            vendor.aboout = aboout
            vendor.website = website
            vendor.save()
            print("website",website)
            print("aboout",aboout)
            print("countryId",countryId)
            print("email",email)
            print("address",address)
            print("vendorName",vendorName)
            # print("image:",image)
            return redirect('vendor_settings')        
        else:
            
            return render (request, 'showout/vendor/vendor_settings.html', context) 
    else:
         return redirect('vendor_login')
 

def add_service(request):
    services = Services.objects.all();
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        if request.method == 'POST':
            serviceId = request.POST['serviceId']
            description = request.POST['description']
            budget = request.POST['budget']
            vendor = Vendors.objects.get(pk=vendorId)
            print("vendor",vendor)
            print("vendorId",vendorId)
            service = Services.objects.get(pk=serviceId)
            VendorServices.objects.create(category=service.category,vendor=vendor,services=service,description=description,budget=budget)
        context = {'services':services}
        return render (request, 'showout/vendor/add_service.html', context)
    else:
        return redirect('vendor_login') 

def edit_service(request,vendorServicesId):
    services = Services.objects.all();
    vendorService = VendorServices.objects.get(pk=vendorServicesId);
    context = {'services':services,'vendorService':vendorService}
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        if request.method == 'POST':
            serviceId = request.POST['serviceId']
            service = Services.objects.get(pk=serviceId)
            description = request.POST['description']
            budget = request.POST['budget']
            vendor = Vendors.objects.get(pk=vendorId)
            vendorService.description = description
            vendorService.budget = budget
            vendorService.vendor = vendor
            vendorService.services = service
            print("vendor",vendor)
            print("vendorId",vendorId)
            vendorService.save()
            return redirect('vendor_services')   
        else:
         return render (request, 'showout/vendor/vendor_edit_service.html', context)    

    else:
        return redirect('vendor_login') 

def delete_view(request):
    if 'vendor_id' in request.session:
        if request.method == 'POST':
            vendorServicesId = request.GET['vendorServicesId']
            print("vendorServicesId",vendorServicesId)
            vendorService = VendorServices.objects.get(pk=vendorServicesId);
            vendorService.delete()
            return redirect('vendor_services') 
        else:
             return redirect('vendor_services') 
    else:
        return redirect('vendor_login') 
