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

def navbar(request):
    cateegories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    context = {'cateegories':cateegories,'services':services,'countries':countries}
    return render(request, 'showout/navbar.html', context)


def sendEmail(request):
    if request.method == 'POST':
        subject = 'Password reset'
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
        subject = 'Password reset'
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


def home(request):  
  
    categories = Category.objects.all()
    countries = Country.objects.all()
    services = Services.objects.all()
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
    context = {'categories':categories,'vendorServices':listVendorServices,'vendors':listVendors,'customer':customer,'services':services,'countries':countries}
   
    return render(request,'showout/customers/home.html', context)

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
        country = Country.objects.get(pk=countryId)
        # address = request.POST['address']
        customer =  Customer.objects.get(email=email)
        if customer is not None:
            messages.error(request, 'Account with this email already exist')
            return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})

        else:    
            if password == confirm_password:
                # Create a new Client instance and save it to the database
                Customer.objects.create(firstName=fname, email=email, password=password, lastName=lname, mobile=mobile,genderId=genderId,country=country,)
                user = authenticate_customer(email, password)
                if user is not None:
                    # Authentication successful, perform login manually
                    request.session['user_id'] = user.customerId  # Store user ID in session
                    # Redirect to a success page or home page
                    confirmationEmail(request,"Registration confirmation",user.email)
                    return redirect('home')
                else:
                    # Authentication failed, display error message
                    messages.error(request, 'Login failed try again')
                    return redirect('customerLogin') 
            else:
                messages.error(request, 'Password does not match')
                return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})


    else:
        return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})

def changePassword(request):
   password = ''
   confirmPassword = '1'
   email = ''
   if request.method == 'GET':
    email =  request.GET['email']
    request.session['customerEmail']  = email;
    return render(request,'showout/customers/changePassword.html')  
   if request.method == 'POST': 
        password =  request.POST['password']
        confirmPassword =  request.POST['confirm_password']
        if password == confirmPassword:
            email = request.session['customerEmail'] 
            customer = Customer.objects.get(email=email)
            if customer is not None:
                customer.password = password
                customer.save()
                print("email",email)
                print("password",password)
                print("confirmPassword",confirmPassword)
                if 'user_id' in request.session:
                    del request.session['user_id'] 
                context = {}
                confirmationEmail(request,"Change Password confirmation",customer.email)
                return redirect('customerLogin') 
            else:
                messages.error(request, 'Account does not exist')
                return render(request,'showout/customers/changePassword.html') 

        else:
          messages.error(request, 'Password does not match')  
          return render(request,'showout/customers/changePassword.html')  
    
        
def vendorPage(request,vendorId):
    vendorServices = VendorServices.objects.all()
    vendor = Vendors.objects.get(pk=vendorId)
    vendorServices = getVendorsServices(vendorServices,vendorId)
    services = Services.objects.all()
    categories = Category.objects.all()
    countries = Country.objects.all()
    context = {'vendorServices':vendorServices,'vendor':vendor,'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/vendorPage.html', context)

def servicePage(request,vendorId,serviceId):
    print("vendorId",  vendorId)
    print("serviceId",  serviceId)
    vendorServices = [];
    vendorServices = VendorServices.objects.all()
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    vendorService = getVendorService(vendorServices,serviceId,vendorId)
    vendorSimilarServices = getVendorSimilarService(vendorServices,serviceId)
    average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
    if average_rating:
       vendorService.rating = average_rating["rating"]
    print("average_rating",average_rating)
    reviewVendoreServices = ReviewVendoreServices.objects.filter(vendorService=vendorService)
    context = {'vendorService':vendorService,'vendorSimilarServices':vendorSimilarServices,'categories':categories,'reviewVendoreServices':reviewVendoreServices,'services':services,'countries':countries}
    return render (request, 'showout/customers/servicePage.html', context)

def viewServices(request,categoryId,categoryName):
    vendorServices = VendorServices.objects.all()
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    servicesByCategory = getVendorsByCategory(vendorServices,categoryId)
    context = {'servicesByCategory':servicesByCategory,'categoryName':categoryName,'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/viewServices.html', context)

def viewVendors(request):
    vendors = Vendors.objects.all()
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    context = {'vendors':vendors,'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/viewVendors.html', context)

def wishlist(request):
    carts =  request.session['cart'] 
    listVendorServices = []
    categories = Category.objects.all()
    vendorServices = VendorServices.objects.all()
    countries = Country.objects.all()
    services = Services.objects.all()
    for cart in carts:
        for vendorService in vendorServices:
            if vendorService.vendorServicesId == int(cart):
                     average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                     if average_rating:
                        vendorService.rating = average_rating["rating"]
                     listVendorServices.append(vendorService)
    context = {'vendorServices':listVendorServices,'categories':categories,'services':services,'countries':countries}
    if request.method == 'POST' and  'user_id' in request.session: 
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
        for vendorService in listVendorServices:
         wishList = WishList.objects.create(vendorService=vendorService, customer=customer, vendor=vendorService.vendor)
         confirmationEmail(request,"Delete Service",vendorService.vendor.email)
   
        wishlistServices =  WishList.objects.filter(customer=customer)
        listWishlistServices  = getWishListVendorService(wishlistServices)
        confirmationEmail(request,"Request Confirmation",customer.email)

        return render (request, 'showout/customers/wishlistHistory.html', {'wishlistServices':listWishlistServices,'categories':categories,'services':services,'countries':countries})

    else:
        return render (request, 'showout/customers/wishlist.html', context)

def wishlistHistory(request):
    wishlistServices = []
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    if 'user_id' in request.session: 
        customerId = request.session['user_id']
        customer = Customer.objects.get(pk=customerId)
        wishlistServices =  WishList.objects.filter(customer=customer)
        listWishlistServices  = getWishListVendorService(wishlistServices)

    return render (request, 'showout/customers/wishlistHistory.html', {'wishlistServices':listWishlistServices,'categories':categories,'services':services,'countries':countries})
    
def topRatedServices(request):
    mostReviewedServices = []
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
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
    return render (request, 'showout/customers/topRatedServices.html', {'mostReviewedServices':mostReviewedServices,'categories':categories,'services':services,'countries':countries})
    
def editProfile(request):
    context = {}
    return render (request, 'showout/customers/editProfile.html', context)

def aboutUS(request):
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    context = {'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/aboutUS.html', context)

def delete_account(request):
    if request.method == 'POST':
        print("accountType",request.GET['accountType'])
        accountType = request.GET['accountType']
        print("accountType",accountType)
        if accountType == "Customer":
            if 'user_id' in request.session:
                user_id = request.session['user_id']
                customer = Customer.objects.get(pk=user_id)
                if customer:
                    del request.session['user_id'] 
                    customer.delete()
                   # Remove user ID from session
                    return redirect('home') 
                else:
                    messages.error(request,"User does not exist")
            else:
                messages.error(request,"User does not exist")
        elif accountType == "Vendor":
            if 'vendor_id' in request.session:
                vendor_id = request.session['vendor_id']
                vendor = Vendors.objects.get(pk=vendor_id)
                if vendor:
                    del request.session['vendor_id'] 
                    vendor.delete()
                        # Remove user ID from session
                    return redirect('vendor_login') 
                else:
                    messages.error(request,"User does not exist")
            else:
                messages.error(request,"User does not exist")

def contactUS(request):
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    context = {'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/contactUS.html', context)

def searchResult(request):
    context = {}
    categories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    review_rating = 0
    if request.method == 'POST':
       query = request.POST.get('query')
       category = request.POST.get('category')
       service = request.POST.get('service')
       review_rating = request.POST.get('review_rating')
       country = request.POST.get('country')
       budget = request.POST.get('budget')
    #    print("review_rating",int(review_rating))
      
    # Perform search or other processing with the query
       searchResultsServices = fetchSearchResults(query,category,service,review_rating,country,budget);
       context = {'searchResultsServices':searchResultsServices,'categories':categories,'services':services,'countries':countries,'review_rating':review_rating}
    #    return HttpResponse(f'Searching for: {query}')

    return render (request, 'showout/customers/searchResult.html',context )

def save_input_to_session(request):
    request.session.modified = True
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data",data)
        input_value = data['inputValue']
        if input_value is not None:
            del request.session['input_value']
            request.session['input_value'] = input_value
            print("input_value",input_value)
            return JsonResponse({'message': 'Input value saved in session.'})
        else:
            return JsonResponse({'error': 'Input value is missing.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def customer_settings(request):
    countries = Country.objects.all()
    genders = Gender.objects.all()
    categories = Category.objects.all()
    services = Services.objects.all()
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        customer = Customer.objects.get(pk=user_id)
        if customer is not None:
            context = {'countries':countries,'customer':customer,'genders':genders,'categories':categories,'services':services}
            if request.method == 'POST':
                # Retrieve registration data from POST request
                email = request.POST['email']
                fname = request.POST['fname']
                lname = request.POST['lname']
                mobile = request.POST['mobile']
                genderId = request.POST['genderId']
                countryId = request.POST['countryId']
                address = request.POST['address']
                country = Country.objects.get(pk=countryId)

                customer.email = email
                customer.firstName = fname
                customer.lastName = lname
                customer.country = country
                customer.address = address
                customer.mobile = mobile
                customer.genderId = genderId
                customer.save()
                confirmationEmail(request,"Profile Update",customer.email)
                print("fname",fname)
                print("genderId",genderId)
                print("countryId",countryId)
                print("email",email)
                print("lname",lname)
                return redirect('customer_settings')        
            else:
                return render (request, 'showout/customers/customer_settings.html', context) 
        else:
             messages.error(request, 'Account does not exist')
             return redirect('customerLogin')   
    else:
         return redirect('customerLogin')



# vendor views

def vendor_login(request):
    if 'vendor_id' in request.session:
        print("hello1")
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        if vendor is not None:
            categories = Category.objects.all()
            vendorServices = VendorServices.objects.all()
            vendors = Vendors.objects.all()
            confirmationEmail(request,"Login Confirmation",vendor.email)
            # context = {'categories':categories,'vendorServices':vendorServices,'vendors':vendors,'customer':customer}
        
            return redirect('vendor_dash')  
        else:
             messages.error(request, 'Account does not exist')
             return redirect('vendor_login')
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
    countries = Country.objects.all()
    genders = Gender.objects.all()
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
        country = Country.objects.get(pk=countryId)
        print("image:",image)
        # Create a new Client instance and save it to the database
        exist = Vendors.objects.get(email=email)
        if exist is not None :
            messages.error(request, 'Account with this email already exist')   
            return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})
        else:
            if confirm_password == password:
                Vendors.objects.create(vendorName=vendorName, email=email, password=password, country=country, mobile=mobile,address=address,genderId=1,image=image)
                vendor = authenticate_vendor(email, password)
                if vendor is not None:
                    # Authentication successful, perform login manually
                    request.session['vendor_id'] = vendor.vendorId  # Store user ID in session
                    # Redirect to a success page or home page
                    confirmationEmail(request,"Sign Up Confirmation",vendor.email)
                    confirmationEmail(request,"New Venor","sylensa.adolf@gmail.com")
                    return redirect('vendor_dash')
                else:
                    # Authentication failed, display error message
                    messages.error(request, 'Invalid email or password')
                    return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})

            else:
                messages.error(request, 'Password does not match')
                return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})


    else:
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
    else:
        return redirect('vendor_login') 

def vendorWishlist(request):
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        wishLists = WishList.objects.filter(vendor=vendor)
       
   
        context = {'wishLists':wishLists}
        return render (request, 'showout/vendor/vendor_wishlist.html', context)
    else:
        return redirect('vendor_login') 
    
def vendor_services(request):
    if 'vendor_id' in request.session:
        vendorId = request.session['vendor_id']
        vendor = Vendors.objects.get(pk=vendorId)
        vendorServices = VendorServices.objects.filter(vendor=vendor)
       
   
        context = {'vendorServices':vendorServices}
        return render (request, 'showout/vendor/vendor_services.html', context)
    else:
        return redirect('vendor_login') 

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

def fetchSearchResults(userSearch,categoryId,serviceId,review_rating,countryId,budget):
    vendorServicesLList = []
    filterCategories = []
    filterServices = []
    filterCountries = []
    filterVendorServices = []
    filterVendors = []

    vendors = Vendors.objects.filter(vendorName__icontains=userSearch)
    print("vendors",vendors)
    categories = Category.objects.filter(categoryName__icontains=userSearch)
    print("categories",categories)
 
   
    if categoryId:
        for c in categories:
          if c.categoryId == int(categoryId):
              filterCategories.append(c)
    else:
        filterCategories = categories

    services = Services.objects.filter(serviceName__icontains=userSearch)
    print("services",services)
    if serviceId:
        for s in services:
            if s.serviceId == int(serviceId):
                filterServices.append(s)
    else:
        filterServices = services

    print("filterServices",filterServices)
    print("serviceId",serviceId)
    
        
    countries = Country.objects.filter(countryName__icontains=userSearch)
    print("countries",countries)
    if countryId:
        for c in countries:
            if c.countryId == countryId:
                filterCountries.append(c)
    else:
        filterCountries = countries

    
    for filterCountry in filterCountries:
        for vendor in vendors:
            if filterCountry.countryId == vendor.countryId:
                filterVendors.append(vendor)

   
    if len(filterVendors) < 1:  
        filterVendors = vendors    


    vendorServices = VendorServices.objects.all()
    for category in filterCategories:
        for vendorService in vendorServices:
            if category.categoryId == vendorService.category.categoryId:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                vendorServicesLList.append(vendorService)

    for ser in filterServices:
        for vendorService in vendorServices:
            if ser.serviceId == vendorService.services.serviceId:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                vendorServicesLList.append(vendorService)

    for vendor in filterVendors:
        for vendorService in vendorServices:
            if vendor.vendorId == vendorService.vendor.vendorId:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                vendorServicesLList.append(vendorService)
    if budget:
        for vendorService in vendorServices:
            if vendorService.budget <= float(budget):
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                vendorServicesLList.append(vendorService)        
 

    # if len(filterVendorServices) < 1:  
    #     filterVendorServices = vendorServices  

    return vendorServicesLList

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
        if password == confirmPassword:
            email = request.session['vendorEmail'] 
            vendor = Vendors.objects.get(email=email)
            vendor.password = password
            vendor.save()
            confirmationEmail(request,"Change password Service",vendor.email)
            print("email",email)
            print("password",password)
            print("confirmPassword",confirmPassword)
            if 'vendor_id' in request.session:
                del request.session['vendor_id']
            context = {}
            return redirect('vendor_login') 
        else: 
            messages.error(request,"Password does not match")
            return render(request,'showout/vendor/vendor_change_password.html')  

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
            country = Country.objects.get(pk=countryId)
            # image = request.FILES.get('image')
            vendor.email = email
            vendor.vendorName = vendorName
            vendor.country = country
            vendor.mobile = mobile
            vendor.address = address
            vendor.aboout = aboout
            vendor.website = website
            vendor.save()
            confirmationEmail(request,"Profile Update",vendor.email)
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
            pdfUpload = request.FILES.get('pdfUpload')
            vendor = Vendors.objects.get(pk=vendorId)
            print("vendor",vendor)
            print("vendorId",vendorId)
            service = Services.objects.get(pk=serviceId)
            VendorServices.objects.create(category=service.category,vendor=vendor,services=service,description=description,budget=budget,pdfUpload=pdfUpload)
            confirmationEmail(request,"Add Service",vendor.email)
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
            pdfUpload = request.FILES.get('pdfUpload')
            vendorService.description = description
            vendorService.budget = budget
            vendorService.vendor = vendor
            vendorService.services = service
            if request.FILES.get('pdfUpload'):
             vendorService.pdfUpload = pdfUpload
            
            print("vendor",vendor)
            print("vendorId",vendorId)
            vendorService.save()
            confirmationEmail(request,"Delete Service",vendorService.vendor.email)
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
            confirmationEmail(request,"Delete Service",vendorService.vendor.email)
            return redirect('vendor_services') 
        else:
             return redirect('vendor_services') 
    else:
        return redirect('vendor_login') 

def confirmationEmail(request,topic,email):
    if request.method == 'POST':
        subject = topic
        to_email =  email # Replace with the recipient's email address
        context = {'link': f'http://127.0.0.1:8000/'}
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
       

