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
from django.conf import settings
import hashlib
import random
from passlib.hash import pbkdf2_sha256


# Create your views here.
emailToken = "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"

def is_user_logged_in(request):
    return 'user_id' in request.session
# this function handles the logout and deletion of session
def my_logout_view(request):
    
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user ID from session
    if 'customerName' in request.session:
        del request.session['customerName'] 
    if 'cart' in request.session:    
        del request.session['cart'] 
    # Redirect to a logout success page or any other desired page
    return redirect('home')

# this function is use for rendering the navbar 
def navbar(request):
    cateegories = Category.objects.all()
    services = Services.objects.all()
    countries = Country.objects.all()
    context = {'cateegories':cateegories,'services':services,'countries':countries}
    return render(request, 'showout/navbar.html', context)

# this function is use for sending email to the ccustomer 
def sendEmail(request):
    if request.method == 'POST': # check if the html form method is post
        subject = 'Password reset'
        to_email =  request.POST['email']  # Replace with the recipient's email address
        cusstomer = Customer.objects.filter(email=to_email.lower())
        if cusstomer:
            context = {'link': f'http://127.0.0.1:8000/changePassword/?email={to_email}'}
            template_path = 'showout/customers/email_template.html'
            messageString = render_to_string(template_path, context)
            from_email = 'hello@showout.studio'  # Replace with your email address
            print("to_email",to_email)   
              # create mail message  
            message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=messageString)
            try:
                 # send email using send grid by passing the token
                sg = SendGridAPIClient(emailToken)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                 # return to email sent page
                return redirect('emailSent')

            except Exception as e:
                print(e)
        messages.error(request, 'Account with this email does not exist')        
        return redirect('reset_password')   

# this function is use for sending email to the vendor 
def sendVendorEmail(request):
    if request.method == 'POST': # check if the html form method is post
        subject = 'Password reset'
        to_email =  request.POST['email']  # Replace with the recipient's email address
        context = {'link': f'http://127.0.0.1:8000/vendor_change_password/?email={to_email}'}
        template_path = 'showout/customers/email_template.html'
        messageString = render_to_string(template_path, context)
        from_email = 'hello@showout.studio'  # Replace with your email address
        print("to_email",to_email)    
          # create mail message  
        message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=messageString)
        try:
            # send email using send grid by passing the token
            sg = SendGridAPIClient(emailToken)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
             # return to email sent page
            return redirect('emailSent')

        except Exception as e:
            print(e)
        return redirect('vendor_password_reset')   

# this function is for rendering the html when the email is sent successfully
def emailSent(request):
   return render(request, 'showout/customers/email_sent.html')

# this function is use for handling vendor logout
def vendor_logout_view(request):
    if 'vendor_id' in request.session:
        del request.session['vendor_id']  # Remove user ID from session
    if 'vendorName' in request.session:
        del request.session['vendorName'] 
    # Redirect to a logout success page or any other desired page
    return redirect('vendor_login')

# this function is use for adding a service to your cart/request
def updateItem(request):
    request.session.modified = True

    data = json.loads(request.body) # get the data through ajax call from cart.js
    # retrieve values from the ajax call
    vendorServicesId = data['vendorServicesId']
    vendorService = VendorServices.objects.get(vendorServicesId=vendorServicesId)
    action = data['action']
    print('Action:', action)
    print('vendorService:', vendorService)
    # deleting the cart in the session
    cart = request.session.get('cart', {})
    # inserting a vendor service id to the session
    cart_item = cart.get(vendorService.vendorServicesId, {'quantity': 0})
    # check if the action is add, then increase the quantity 
    if action == 'add':
      cart_item['quantity'] += 1
        # check if the action is remove, then decrease the quantity 
    elif action == 'remove':
      cart_item['quantity'] -= 1
    cart[vendorService.vendorServicesId] = cart_item
    request.session['cart'] = cart
      # if the quantoty is less than  or equall to 0, then delete the vendor service id
    if cart_item['quantity'] <= 0 :
        del  request.session['cart'][vendorService.vendorServicesId] 
        del  request.session['cart'][str(vendorService.vendorServicesId)]
        print("ccart",request.session['cart'])

    return JsonResponse('Item was added', safe=False)

# this function is use for handling the review of vendor services
def updateRating(request):
    if 'user_id' in request.session: # check if the user is loggedin 
        # this block is to get the values coming frorm the reeview form
        data = json.loads(request.body)
        ratingValue = data['ratingValue']
        vendorServicesId = data['vendorServicesId']
        customerId = request.session['user_id']
        review = data['review']
        # get the vendor service 
        vendorService = VendorServices.objects.get(vendorServicesId=vendorServicesId)
         # get the customer  
        customer = Customer.objects.get(customerId=customerId)
        print("ratingValue",ratingValue)
        print("vendorServicesId",vendorServicesId)
        print("customerId",customerId)
        print("review",review)
        # save customer reeview 
        reviewVendoreServices = ReviewVendoreServices.objects.create(vendorService=vendorService, customer=customer, rating=ratingValue, review=review,vendorServicesId=vendorServicesId,vendor=vendorService.vendor)

    # return success message to the html
    return JsonResponse('Service rated succcessfully', safe=False)

# this function is use for handling the customer login 
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
                request.session['customerName'] = user.firstName + " " +  user.lastName
                # Redirect to a success page or home page
                return redirect('home')
            else:
                # Authentication failed, display error message
                messages.error(request, 'Invalid email or password')
        return render(request, 'showout/customers/login.html')


# this function is use for handling the customer home page
def home(request):  
    listCategories = [] # varibal to hold the list of categories
    categories = Category.objects.all() # this line of code fetches all categories from the categories table
    countries = Country.objects.all() # this line of code fetches all countries from the countries table
    services = Services.objects.all() # this section fetcched all services from the service table
    vendorServices = filterVendorServices(categories) # this function return the first 4 VendorServices for each cateegory. the function expect list of categories as a parameter
    listVendorServices = appRatingToService(vendorServices) # this function acceept list of vendor services and assign the avearge rating value to each vendor service and return the list of vendor services
    vendors = Vendors.objects.all() # this line of code fetches all vendors
    listVendors = appRatingToVendors(vendors) # this function accept list of vendors and assign average rating of al veendor service created by each vendor
    listCategories = filterByCategory(categories) # this function accept categories and retuurns list of vendor services for each category

    context = {'categories':listCategories,'vendorServices':listVendorServices,'vendors':listVendors,'services':services,'countries':countries}
   
    return render(request,'showout/customers/home.html', context)

# this function is use for rendering the reset password html
def resetPassword(request):
    context = {}
    return render (request, 'showout/customers/resetPassword.html', context)

# this function is use for handling the customer registration
def register(request):

    countries = Country.objects.all() # get all countries from country table
    genders = Gender.objects.all() # get all gender from gender table
    country = None
    if request.method == 'POST': # check if the html form method is POST
        # Retrieve registration data from POST request
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        mobile = request.POST['mobile']
        genderId = request.POST['genderId']
        countryId = request.POST['countryId']
        if int(genderId) == 0:
            genderId = 0
        confirm_password = request.POST['confirm_password']
        password = request.POST['password']
        # encrypt the password
        hashed_password = pbkdf2_sha256.hash(password)
        if int(countryId) != 0:
         country = Country.objects.get(pk=countryId)
         # to check if the password leength is bigger than 6
        if len(password) > 6 and len(confirm_password) > 6:   
            try:
                # cheeck if theres an accouunt with this email
                customer =  Customer.objects.get(email=email.lower())
                messages.error(request, 'Account with this email already exist')
                return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})
           
            except Customer.DoesNotExist:  
                # if the customer does not exist, i check if the password andd confirm password are the same
                if password == confirm_password:
                    # Create a new Customer instance and save it to the database
                    Customer.objects.create(firstName=fname, email=email.lower(), password=password, lastName=lname, mobile=mobile,genderId=genderId,country=country,hashed_password=hashed_password)
                    user = authenticate_customer(email, password) # this function authenticate the user by accepting email and password and return a customeer object
                    if user is not None:
                        # Authentication successful, perform login manually
                        request.session['user_id'] = user.customerId  # Store user ID in session
                        request.session['customerName'] = user.firstName + " " +  user.lastName
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
              messages.error(request, 'Password length should be atleast 7 characters')  
              return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})
           

    else:
        return render(request, 'showout/customers/register.html',{'genders':genders,'countries':countries})

# this function is use for handling customer change password
def changePassword(request):
   password = ''
   confirmPassword = '1'
   email = ''
   if request.method == 'GET': # check if the method is get
    email =  request.GET['email'] # retireve tthe value 
    request.session['customerEmail']  = email # assign a value to the session
    return render(request,'showout/customers/changePassword.html')  
   if request.method == 'POST': # check if the method is post
        password =  request.POST['password'] # retireve the value 
        confirmPassword =  request.POST['confirm_password'] # retireve tthe value 
        hashed_password = pbkdf2_sha256.hash(password) # encrypt the password
        if len(password) > 6 and len(confirmPassword) > 6:   # checkk if the password leength is bigger than 6  
            if password == confirmPassword: # check if thee password and confirm passwords are equal
                email = request.session['customerEmail'] # get the value frorm the session
                try:
                    customer =  Customer.objects.get(email=email.lower()) # get the customer information
                    customer.password = password
                    customer.hashed_password = hashed_password
                    customer.save() # update the customer information
                    print("email",email)
                    print("password",password)
                    print("confirmPassword",confirmPassword)
                    if 'user_id' in request.session: # check if the customer is lloggedin
                        del request.session['user_id'] # deelete the customer session
                    context = {}
                    confirmationEmail(request,"Change Password confirmation",customer.email) # send a confirmation email
                    return redirect('customerLogin') # redirect the customer to the login page
                except Customer.DoesNotExist: 
                    messages.error(request, 'Account does not exist')
                    return render(request,'showout/customers/changePassword.html') 

            else:
                messages.error(request, 'Password does not match')  
                return render(request,'showout/customers/changePassword.html')  
        else:
                messages.error(request, 'Password length should be atleast 7 characters')  
                return render(request,'showout/customers/changePassword.html')  

# this function is use for rendring vendor page in  the customer website        
def vendorPage(request,vendorId):
    vendorServices = VendorServices.objects.all() # get all vendor servicess
    vendor = Vendors.objects.get(pk=vendorId) # get all vendors
    vendorServices = getVendorsServices(vendorServices,vendorId) # get all vendor services assign to a specific vendor
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    context = {'vendorServices':vendorServices,'vendor':vendor,'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/vendorPage.html', context)

# this function is use for rendring service page in  the customer website
def servicePage(request,vendorId,serviceId):
    print("vendorId",  vendorId)
    print("serviceId",  serviceId)
    vendorServices = []
    vendorServices = VendorServices.objects.all() # get all vendor servicess
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    vendorService = getVendorService(vendorServices,serviceId,vendorId) # get all vendor services assign to a specific vendor
    print("vendorService vendor",vendorService.vendor.vendorId)
    vendorSimilarServices = getVendorSimilarService(vendorServices,vendorService) # get recommendded services
    average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating')) # average rating of each services
    if average_rating:
       vendorService.rating = average_rating["rating"]
    print("average_rating",average_rating)
    reviewVendoreServices = ReviewVendoreServices.objects.filter(vendorService=vendorService) # retrieve vendors servies by passing vendor service 
    context = {'vendorService':vendorService,'vendorSimilarServices':vendorSimilarServices,'categories':categories,'reviewVendoreServices':reviewVendoreServices,'services':services,'countries':countries}
    return render (request, 'showout/customers/servicePage.html', context)

# this function is use for rendring list of services by category
def viewServices(request,categoryId,categoryName):
    vendorServices = VendorServices.objects.all()  # get all vendor servicess
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    servicesByCategory = getVendorsByCategory(vendorServices,categoryId) # get vendor service by ccategory
    context = {'servicesByCategory':servicesByCategory,'categoryName':categoryName,'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/viewServices.html', context)

# this function is use for rendring list of vendors 
def viewVendors(request):
    vendors = Vendors.objects.all() # gdt all vendors
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    context = {'vendors':vendors,'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/viewVendors.html', context)

# this function is use for rendring the customerr request page in the customer website
def requests(request):
    vendorServices = VendorServices.objects.all() # fetch all vendor services
    categories = Category.objects.all()  # this line of code fetches all categories from the categories table
    services = Services.objects.all()  # this section fetcched all services from the service table
    countries = Country.objects.all() # this line of code fetches all countries from the countries table
   
    listVendorServices = []
    context = {}
    if 'cart' in request.session: # check if theree is item in the cart session
        carts =  request.session['cart'] # get thee carts from the session
        for cart in carts: # loop through the carts

            # loop through the vendor services
            for vendorService in vendorServices: 
                # cheeck if the vendor service id in the cart is equal to any of the vendor services
                if vendorService.vendorServicesId == int(cart):
                        # assign average rating to the vendor service
                        average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                        if average_rating:
                            vendorService.rating = average_rating["rating"]
                        listVendorServices.append(vendorService)
        context = {'vendorServices':listVendorServices,'categories':categories,'services':services,'countries':countries}
        print("context",context)
        # submit a user request to vendors
        if request.method == 'POST' and  'user_id' in request.session: # check if the customer is loggedin andd the method is post
            customerId = request.session['user_id'] # get customer id from the session
            customer = Customer.objects.get(pk=customerId) # get customer by primary key
            for vendorService in listVendorServices:
                # insert customer reequest into the CustomerRequests model table
                wishList = CustomerRequests.objects.create(vendorService=vendorService, customer=customer, vendor=vendorService.vendor)
                # send confirmation email to veendor
                confirmationEmail(request,"Request email",vendorService.vendor.email)
        
            wishlistServices =  CustomerRequests.objects.filter(customer=customer)
            listWishlistServices  = getWishListVendorService(wishlistServices)
              # send confirmation email to customer
            confirmationEmail(request,"Request Confirmation",customer.email)

            return render (request, 'showout/customers/requestsHistory.html', {'wishlistServices':listWishlistServices,'categories':categories,'services':services,'countries':countries})

        else:
            return render (request, 'showout/customers/requests.html', context)
    else:
        context = {'vendorServices':listVendorServices,'categories':categories,'services':services,'countries':countries}

        return render (request, 'showout/customers/requests.html', context)
    

# this function is use for rendering the customer request history in the customer website
def requestsHistory(request):
    wishlistServices = []
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    if 'user_id' in request.session: # check if the user is logged in
        customerId = request.session['user_id'] # pass the session value to cusstomer id
        customer = Customer.objects.get(pk=customerId) # get a specific customer information
        wishlistServices =  CustomerRequests.objects.filter(customer=customer) # fetch all request of a specific customer
        listWishlistServices  = getWishListVendorService(wishlistServices) # this function assign average rating to each vendor service

    return render (request, 'showout/customers/requestsHistory.html', {'wishlistServices':listWishlistServices,'categories':categories,'services':services,'countries':countries})

# this function is use for rendering the top rated orr reviewed services in the customer website      
def topRatedServices(request):
    mostReviewedServices = []
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    reviews_grouped = ReviewVendoreServices.objects.values('vendorService').annotate(rating=Avg('rating')) # get reviewe services
    most_reviewed_services = [  
    ReviewVendoreServices.objects.filter(vendorService=item['vendorService']).first() # filter reviewedd services
    for item in reviews_grouped
        ]
    for most_reviewed_service in most_reviewed_services:
        average_rating = ReviewVendoreServices.objects.filter(vendorService=most_reviewed_service.vendorService).aggregate(rating=Avg('rating')) # fetch average rating of each reviewed services
        if average_rating:
            print("most_reviewed_service.vendorService",most_reviewed_service.vendorService)
            most_reviewed_service.vendorService.rating = average_rating["rating"]
            mostReviewedServices.append(most_reviewed_service)
    print("mostReviewedServices",most_reviewed_services)
    return render (request, 'showout/customers/topRatedServices.html', {'mostReviewedServices':mostReviewedServices,'categories':categories,'services':services,'countries':countries})
    
# this function is use for rendering edit profile  
def editProfile(request):
    context = {}
    return render (request, 'showout/customers/editProfile.html', context)

# this function is use for rendering about us page  in the customer website
def aboutUS(request):
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    context = {'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/aboutUS.html', context)

# this function is use for deleting customer and vendor account
def delete_account(request):
    if request.method == 'POST': # check if it a post method
        print("accountType",request.GET['accountType'])
        accountType = request.GET['accountType'] # retirrieve the data
        print("accountType",accountType)
        if accountType == "Customer": # check if it is the customer who is deleting their account
            if 'user_id' in request.session: # check if the customer is logged in
                user_id = request.session['user_id'] # get customer id from the session
                try:
                    # get the customeer information andd delete the customer and the sessions
                    customer = Customer.objects.get(pk=user_id)
                    del request.session['user_id'] # delete customer id
                    del request.session['customerName'] # delete customer name 
                    customer.delete() # delete the customers
                   # Remove user ID from session
                    return redirect('home') 
                    
                except:
                    del request.session['user_id'] # delete customer id
                    del request.session['customerName'] # delete customer name 
                    messages.error(request,"User does not exist")
                    return redirect('vendor_login') 

            else:
                messages.error(request,"User does not exist")
        elif accountType == "Vendor":
            if 'vendor_id' in request.session: # check if the vendor is logged in
                try:
                    vendor_id = request.session['vendor_id'] # get vendor id from the session
                     # get the Vendor information andd delete the Vendor and the sessions
                    vendor = Vendors.objects.get(pk=vendor_id)
                    del request.session['vendor_id']  # delete vendor id
                    del request.session['vendorName'] # delete vendorName name 
                    vendor.delete()  # delete the customers
                        # Remove user ID from session
                    return redirect('vendor_login') 
                except:
                    del request.session['vendor_id']  # delete vendor id
                    del request.session['vendorName'] # delete vendorName name 
                    messages.error(request,"User does not exist")
                    return redirect('vendor_login')                 
               
            else:
                messages.error(request,"User does not exist")

# this function is use for rendering contact us page  in the customer website
def contactUS(request):
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    context = {'categories':categories,'services':services,'countries':countries}
    return render (request, 'showout/customers/contactUS.html', context)

# this function is use for rendering seearch result page  in the customer website
def searchResult(request):
    context = {}
    vendorRecommendedServices = []
    categories = Category.objects.all()  # this line of code fetches all categories from the categories table
    services = Services.objects.all()  # this section fetcched all services from the service table
    countries = Country.objects.all() # this line of code fetches all countries from the countries table
   
    review_rating = 0
    if request.method == 'POST': # this line of code is to check if the form method is post
       # this block of code is to get the values coming from the search filter modal form
       query = request.POST.get('query') 
       category = request.POST.get('category')
       service = request.POST.get('service')
       review_rating = request.POST.get('review')
       country = request.POST.get('country')
       budget = request.POST.get('budget')
       print("review_rating",int(review_rating))
      
    # Perform search or other processing with the query
       searchResultsServices = fetchSearchResults(query,category,service,country,budget,review_rating)
       print('searchResultsServices',searchResultsServices)
         # fetch all vendor services with limit 8
       vendorServices = VendorServices.objects.all()[:8]
        # assigning average rating to each vendor service by passing vendorServices to the function appRatingToService
       vendorSimilarServices = appRatingToService(vendorServices)
       # this block of code is to filter recommenced service to the customer base on the service they click 
       for vendorSimilarService in vendorSimilarServices:
           if vendorSimilarService not in searchResultsServices:
             vendorRecommendedServices.append(vendorSimilarService)

               
    context = {'searchResultsServices':searchResultsServices,'categories':categories,'services':services,'countries':countries,'review_rating':review_rating,'vendorSimilarServices':vendorRecommendedServices}
    #    return HttpResponse(f'Searching for: {query}')

    return render (request, 'showout/customers/searchResult.html',context )

# this function is use for saving input sessions
def save_input_to_session(request):
    request.session.modified = True
    if request.method == 'POST': # check if the method is post
        data = json.loads(request.body) # retirreve the data from ajax call
        print("data",data)
        input_value = data['inputValue']
        if input_value is not None:
            # del request.session['input_value']
            request.session['input_value'] = input_value
            print("input_value",input_value)
            return JsonResponse({'message': 'Input value saved in session.'})
        else:
            return JsonResponse({'error': 'Input value is missing.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# this function is use for rendering customer settings page in the customer website
def customer_settings(request):
    genders = Gender.objects.all()# get all vendors
    services = Services.objects.all() # get all services
    categories = Category.objects.all() # get all categories
    countries = Country.objects.all() # get all countries
    country = None
    if 'user_id' in request.session: # check if the customer is loggedd in
        user_id = request.session['user_id']
        try:
            customer = Customer.objects.get(pk=user_id) # get a specific customer information
            context = {'countries':countries,'customer':customer,'genders':genders,'categories':categories,'services':services}
            if request.method == 'POST': # check if the form method is post
                # Retrieve registration data from POST request
                email = request.POST['email']
                fname = request.POST['fname']
                lname = request.POST['lname']
                mobile = request.POST['mobile']

                if email and fname and lname and mobile: # check if these values are not empty
                    genderId = request.POST['genderId']
                    if int(genderId) == 0:
                        genderId = 0
                    countryId = request.POST['countryId']
                    if int(countryId) != 0:
                     country = Country.objects.get(pk=countryId) # get specific country data
                    address = request.POST['address']
                    country = Country.objects.get(pk=countryId)

                    # assign the values to the customer object
                    customer.email = email.lower()
                    customer.firstName = fname
                    customer.lastName = lname
                    customer.country = country
                    customer.address = address
                    customer.mobile = mobile
                    customer.genderId = genderId
                    customer.save() # save or update the customer information
                    confirmationEmail(request,"Profile Update",customer.email) # send email confirmation
                    print("fname",fname)
                    print("genderId",genderId)
                    print("countryId",countryId)
                    print("email",email)
                    print("lname",lname)
                    messages.error(request, 'Information updated successfully') 
                    return redirect('customer_settings')  
                else:
                   messages.error(request, 'All fields are reequired')   
                   return render (request, 'showout/customers/customer_settings.html', context)      
            else:
                return render (request, 'showout/customers/customer_settings.html', context) 
        except:
             messages.error(request, 'Account does not exist')
             return render (request, 'showout/customers/customer_settings.html', context) 
  
    else:
         return redirect('customerLogin')



# vendor views

# this function is use for rendering vendor login page 
def vendor_login(request):
    if 'vendor_id' in request.session: # check if the vendor is loggedin
        vendorId = request.session['vendor_id'] # get the vendor id from the session
        try:
            vendor = Vendors.objects.get(pk=vendorId) # get vendor by passsing the vendor id to the primary kkey
            return redirect('vendor_dash')  
        except:
             print("hello1")
             del  request.session['vendor_id'] 
             return redirect('vendor_login')
    else:
       
        if request.method == 'POST': # check if the method is post from the html form method
            print("hello")
            # retireve values from the form
            email = request.POST['email']
            password = request.POST['password']
            # authenticate the vendor
            vendor = authenticate_vendor(email, password)
            if vendor is not None:
                # Authentication successful, perform login manually
                request.session['vendor_id'] = vendor.vendorId  # Store user ID in session
                request.session['vendorName'] = vendor.vendorName
                # Redirect to a success page or home page
                confirmationEmail(request,"Login Confirmation",vendor.email)
                return redirect('vendor_dash')
            else:
                # Authentication failed, display error message
                print('Invalid email or password')
                messages.error(request, 'Invalid email or password')
        return render(request, 'showout/vendor/vendor_login.html')

# this function is use for rendering vendor sign up page 
def vendor_sign_up(request):
    countries = Country.objects.all() # get all countries
    country = None
    genders = Gender.objects.all() # get all gender
    if request.method == 'POST': # ccheckk if the form post method is post
        # Retrieve registration data from POST request
        email = request.POST['email']
        vendorName = request.POST['vendorName']
        mobile = request.POST['mobile']
        countryId = request.POST['countryId']
        if int(countryId) != 0:
         country = Country.objects.get(pk=countryId)
        address = request.POST['address']
        confirm_password = request.POST['confirm_password']
        password = request.POST['password']
         # encrypt the password
        hashed_password = pbkdf2_sha256.hash(password)
        image = request.FILES.get('image')
       
        print("image:",image)
         # to check if the password leength is bigger than 6
        if len(password) > 6 and len(confirm_password) > 6: 
            try :
                exist = Vendors.objects.get(email=email.lower())
                messages.error(request, 'Account with this email already exist')   
                return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})
            except:
                  # if the customer does not exist, i check if the password andd confirm password are the same
                if confirm_password == password:
                     # Create a new Vendor instance and save it to the database
                    Vendors.objects.create(vendorName=vendorName, email=email.lower(), password=password, country=country, mobile=mobile,address=address,genderId=1,image=image,hashed_password=hashed_password)
                    vendor = authenticate_vendor(email, password)
                     # if the vendor does not exist, 
                    if vendor is not None:
                        # Authentication successful, perform login manually
                        request.session['vendor_id'] = vendor.vendorId  # Store user ID in session
                        request.session['vendorName'] = vendor.vendorName
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
             messages.error(request, 'Password length should be atleast 7 characters')
             return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})



    else:
        return render(request, 'showout/vendor/vendor_sign_up.html',{'countries':countries,'genders':genders})

# this function is use for rendering vendor customer list page in the vendor website
def customerlist(request):
    if 'vendor_id' in request.session: # check if the vendor is loggein 
        vendorId = request.session['vendor_id'] # retrieve vendor id
        vendor = Vendors.objects.get(pk=vendorId) # get vendor information
        wishLists = CustomerRequests.objects.filter(vendor=vendor) # retirieve vendor request
        customers = wishLists.values('customer').annotate(count=Count('customer')) # retrieve customers from requests
        # get all ccustomers from the customer request
        allCustomers = [  
        CustomerRequests.objects.filter(customer=item['customer']).first()
        for item in customers
            ]
        print("wishLists",allCustomers)
   
        context = {'wishLists':allCustomers}
        return render (request, 'showout/vendor/customerlist.html', context)
    else:
        return redirect('vendor_login') 

# this function is use for rendering vendor request list page in the vendor website
def vendorWishlist(request):
    if 'vendor_id' in request.session: # check if the vendor is loggein 
        vendorId = request.session['vendor_id'] # retrieve vendor id
        vendor = Vendors.objects.get(pk=vendorId) # get vendor information
        wishLists = CustomerRequests.objects.filter(vendor=vendor) # retirieve vendor request
       
   
        context = {'wishLists':wishLists}
        return render (request, 'showout/vendor/vendor_wishlist.html', context)
    else:
        return redirect('vendor_login') 
    
# this function is use for rendering vendor's service list page in the vendor website    
def vendor_services(request):
    if 'vendor_id' in request.session: # check if the vendor is loggein 
        vendorId = request.session['vendor_id'] # retrieve vendor id
        vendor = Vendors.objects.get(pk=vendorId) # get vendor information
        vendorServices = VendorServices.objects.filter(vendor=vendor) # retirieve vendor services
       
   
        context = {'vendorServices':vendorServices}
        return render (request, 'showout/vendor/vendor_services.html', context)
    else:
        return redirect('vendor_login') 

# this function is use for rendering vendor dashboard page in the vendor website
def vendor_dash(request):
    listVendorServices = []
    if 'vendor_id' in request.session: # check if the vendor is loggedin 
        vendorId = request.session['vendor_id'] # get vendor id from sesssion
        vendor = Vendors.objects.get(pk=vendorId) # retirieve vendor information
        print("vendor",vendor)
        print("vendorId",vendorId)
        # fetch vendor service for the loggedin vendor
        vendorServices = VendorServices.objects.filter(vendor=vendor) 
        # assign ratings to the vendor services
        listVendorServices = appRatingToService(vendorServices)
        # feetch all request for loggedin vendor
        wishLists = CustomerRequests.objects.filter(vendor=vendor)
           # feetch all customers for loggedin vendor
        customers = wishLists.values('customer').annotate(count=Count('customer'))
        print("customers",customers)
        return render (request, 'showout/vendor/vendor_dash.html', {"vendorServices":listVendorServices, "wishLists":wishLists,"customers":customers})

    else:
        return redirect('vendor_login') 

def document(request):
    context = {}
    return render (request, 'showout/vendor/document.html', context)

# function to assign average rating to vendor service in request list
def getWishListVendorService(wishlistServices):
    # this function assign average rating to each vendor service 
    listWishlistService = []
    for wishlistService in wishlistServices:
            average_rating = ReviewVendoreServices.objects.filter(vendorService=wishlistService.vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                wishlistService.vendorService.rating = average_rating["rating"]
            listWishlistService.append(wishlistService)
        
    
    return listWishlistService

# function to assign average rating to vendor service and return the vendor service       
def getVendorService(vendorServices,serviceId,vendorId):
   for vendorService in vendorServices: # loop through the vendor services
        if vendorService.vendor: # check if the vendor exist
            if vendorService.services.serviceId == serviceId and vendorService.vendor.vendorId == vendorId: # check if the vendor id and the service id is the same inside the venor service
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating')) # average rating 
                if average_rating:
                    vendorService.rating = average_rating["rating"] # assign average rating
                return vendorService # return the vendor service
                break

# function to assign average rating to vendor service  
def appRatingToService(vendorServices):
    listVendorServices = []
    for vendorService in vendorServices:
        # this block of code is to assign the average rating for each vendor service 
        average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
        if average_rating:
            vendorService.rating = average_rating["rating"] # this is where the average rating valu is assign to the vendor service
        listVendorServices.append(vendorService)
    # return the list of VendorServices
    return listVendorServices

# function to assign average rating to vendors and return  vendors  
def appRatingToVendors(vendors):
    listVendors = []
    for vendor in vendors:
        # this block of code  assign average rating of all vendor service created by each vendor
        average_rating = ReviewVendoreServices.objects.filter(vendor=vendor).aggregate(rating=Avg('rating'))
        if average_rating:
            vendor.rating = average_rating["rating"]
        listVendors.append(vendor)
    # return list of vendors
    return listVendors

# function to filter vendor serrvice by category 
def filterByCategory(category):
    vendorServervices = []
    for cat in category:
        # this bllock of code fetch all vendor service base on category
        vendorServ = VendorServices.objects.filter(category=cat)
        if vendorServ:
            vendorServervices.append(cat)
        
    # return list vendorServervice
    return vendorServervices

# function to filter vendor serrvice by category and return first 4 vendor service or each category
def filterVendorServices(category):
    vendoerServices = [] # variballe to hold list of services
    for cat in category:
        vendorServ = VendorServices.objects.filter(category=cat)[:4] # this line of code fetches the first 4 vendor services for each category from the VendorService table
        if vendorServ: # this line is to check if the vendorServ is not empty
            vendoerServices.extend(vendorServ) # this line of code append all the data from vendorServ to vendoerServices
        
    return vendoerServices # vendoerServices is return by the function

# function to fetch similar vendor service
def getVendorSimilarService(vendorServices,vendorSelectedService):
  # this block of code is return similar vendor services as recommended venodr service, meaning service in the same categories
   vendorSimilarServices = []
   for vendorService in vendorServices: 
        print("vendorSelectedService.services.category",vendorService.services.category.categoryId)
        # check if the services are in the same ccategory
        if vendorService.services.category.categoryId == vendorSelectedService.services.category.categoryId and vendorService.services.serviceId != vendorSelectedService.services.serviceId:
            average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                vendorService.rating = average_rating["rating"]
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices # return recommended service 

# get vendor service for a specific vendor
def getVendorsServices(vendorServices,vendorId):
   vendorSimilarServices = []
   for vendorService in vendorServices: # loop through the vendor services
        print("vendorService.vendor",vendorService.vendor)
        if vendorService.vendor: # check if the vendor exist
            if vendorService.vendor.vendorId == vendorId: # check if the vednor id is the same as the vendor who uploaded the vendor service
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating')) # fetch average rating for each vendor services
                if average_rating:
                    vendorService.rating = average_rating["rating"] # assign average rating for each vendor services
                vendorSimilarServices.append(vendorService)
                print("getVendorSimilarService",vendorSimilarServices)
   return vendorSimilarServices # return the list of vendor services

# function to filter vendor serrvice by category 
def getVendorsByCategory(vendorServices,categoryId):
   # this function is to get vendors servies by categories 
   vendorSimilarServices = []
   for vendorService in vendorServices: # loop through the service
        if vendorService.category.categoryId == categoryId: # check if the categories are the same 
            average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
            if average_rating:
                vendorService.rating = average_rating["rating"]
            vendorSimilarServices.append(vendorService)
            print("getVendorSimilarService",vendorSimilarServices)
            # return vendor services
   return vendorSimilarServices

# function to handle search filtering
def fetchSearchResults(userSearch,categoryId,serviceId,countryId,budget,review_rating):
    vendorServicesLList = []
    filterCategories = []
    filterServices = []
    filterCountries = []
    filterVendorServices = []
    filterVendors = []
    
    # this block of code check if the userSearch is not eempty, then fetch all vendors with such name from the filter search query
    if userSearch:    
        vendors = Vendors.objects.filter(vendorName__icontains=userSearch)
        if vendors:
            filterVendors = vendors
 
   # this block of code check if the customer selected a category, then fetch all cateegories base on the category selected
    if categoryId != "0":
        filterCategories =  Category.objects.filter(pk=int(categoryId))

     # this block of code check if the customer selected a service, then fetch all services base on the service selected
    if serviceId != "0":
        filterServices = Services.objects.filter(pk=int(serviceId))

       # this block of code check if the customer selected a country, then fetch all countries base on the country selected
    if countryId != "0":
       filterCountries = Country.objects.filter(pk=int(countryId))
    
    # fetch all vendor services
    vendorServices = VendorServices.objects.all()

    # filter the vendor service base on the categories selected
    for category in filterCategories:
        for vendorService in vendorServices:
            if category.categoryId == vendorService.category.categoryId:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                if vendorService not in vendorServicesLList:
                    vendorServicesLList.append(vendorService) 

   # filter the vendor service base on the services selected
    for ser in filterServices:
        for vendorService in vendorServices:
            if ser.serviceId == vendorService.services.serviceId:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                if vendorService not in vendorServicesLList:
                    vendorServicesLList.append(vendorService) 

   # filter the vendor service base on the vendors
    for vendor in filterVendors:
        for vendorService in vendorServices:
            if vendorService.vendor:
                if vendor.vendorId == vendorService.vendor.vendorId:
                    average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                    if average_rating:
                        vendorService.rating = average_rating["rating"]
                    if vendorService not in vendorServicesLList:
                        vendorServicesLList.append(vendorService) 
      # filter the vendor service base on the budget entered
    if budget:
        for vendorService in vendorServices:
            if vendorService.budget <= float(budget):
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    vendorService.rating = average_rating["rating"]
                if vendorService not in vendorServicesLList:
                    vendorServicesLList.append(vendorService)        
 
  # filter the vendor service base on the ratings selected
    if review_rating != '0':  
        for vendorService in vendorServices:
                average_rating = ReviewVendoreServices.objects.filter(vendorService=vendorService).aggregate(rating=Avg('rating'))
                if average_rating:
                    print("average_rating",average_rating)
                    if average_rating["rating"]:
                        vendorService.rating = int(average_rating["rating"])
                        if vendorService.rating >= int(review_rating):
                            print("hey no")
                            if vendorService not in vendorServicesLList:
                              vendorServicesLList.append(vendorService) 
                    elif vendorService in vendorServicesLList:
                            vendorServicesLList.remove(vendorService)


    return vendorServicesLList

# function to authenticate customer
def authenticate_customer(email, password):
    # function check if the customer exist and compare the password also matches the existing one, 
    # if not then return None else return the customer objeect
    try:
        customer = Customer.objects.get(email=email.lower())
        if customer.password == password and passlib_encryption_verify(password, customer.hashed_password):
            return customer
    except Customer.DoesNotExist:
        return None
    
# function to authenticate vendor    
def authenticate_vendor(email, password):
        # function check if the vendor exist and compare the password also matches the existing one, 
        # if not then return None else return the vendor objeect
    try:
        vendor = Vendors.objects.get(email=email.lower())
        
        if vendor.password == password  and passlib_encryption_verify(password, vendor.hashed_password):
                return vendor
    except Vendors.DoesNotExist:
        return None
    
# function to verify encrypted password   
def passlib_encryption_verify(raw_password, enc_password):
	if raw_password and enc_password:
		# verifying the password
		response = pbkdf2_sha256.verify(raw_password, enc_password)
	else:
		response = None;
	
	return response

# function for rendering vender password reset page
def vendor_password_reset(request):
    context = {}
       # render the html
    return render (request, 'showout/vendor/vendor_password_reset.html', context)

# function for rendering vender change password page
def vendor_change_password(request):
  password = ''
  confirmPassword = ''
  email = ''
  if request.method == 'GET': # check if the method is get
    email =  request.GET['email']  # retireve tthe value 
    request.session['vendorEmail']  = email # assign a value to the session
    return render(request,'showout/vendor/vendor_change_password.html')  
  if request.method == 'POST': # check if the method is post
        password =  request.POST['password'] # retireve the value 
        confirmPassword =  request.POST['confirm_password'] # retireve the value 
        hashed_password = pbkdf2_sha256.hash(password) # encrypt password  
        if len(password) > 6 and len(confirmPassword) > 6:  # checkk if the password leength is bigger than 6  
            if password == confirmPassword:  # check if thee password and confirm passwords are equal
                email = request.session['vendorEmail']  # get the value frorm the session
                try:
                    vendor = Vendors.objects.get(email=email.lower()) # get the customer information
                    vendor.password = password
                    vendor.hashed_password = hashed_password
                    vendor.save() # update the customer information
                    confirmationEmail(request,"Change password Service",vendor.email) # send a confirmation email
                    print("email",email)
                    print("password",password)
                    print("confirmPassword",confirmPassword)
                    if 'vendor_id' in request.session:
                        del request.session['vendor_id']
                    context = {}
                    return redirect('vendor_login') 
                except:
                    messages.error(request,"Account does not exist")
                    return render(request,'showout/vendor/vendor_change_password.html') 

            else: 
                messages.error(request,"Password does not match")
                return render(request,'showout/vendor/vendor_change_password.html')  
        else:
                messages.error(request, 'Password length should be atleast 7 characters')  

                return render(request,'showout/vendor/vendor_change_password.html')  

# function for rendering vender settings page
def vendor_settings(request):
    countries = Country.objects.all()
    country = None
    if 'vendor_id' in request.session:  # check if the customer is loggedd in
        vendorId = request.session['vendor_id']
        try:
            vendor = Vendors.objects.get(pk=vendorId) # get a specific vendor information
            context = {'countries':countries,'vendor':vendor}
            if request.method == 'POST':  # check if the form method is post
                # Retrieve registration data from POST request
                email = request.POST['email']
                vendorName = request.POST['vendorName']
                mobile = request.POST['mobile']
                countryId = request.POST['countryId']
                if int(countryId) != 0:
                 country = Country.objects.get(pk=countryId)
                address = request.POST['address']
                aboout = request.POST['aboout']
                website = request.POST['website']
                if email and vendorName and mobile and address and aboout and website:
                
                    # image = request.FILES.get('image')
                    vendor.email = email.lower()
                    vendor.vendorName = vendorName
                    vendor.country = country
                    vendor.mobile = mobile
                    vendor.address = address
                    vendor.aboout = aboout
                    vendor.website = website
                    vendor.save() # save or update the vendor information
                    confirmationEmail(request,"Profile Update",vendor.email)
                    print("website",website)
                    print("aboout",aboout)
                    print("countryId",countryId)
                    print("email",email)
                    print("address",address)
                    print("vendorName",vendorName)
                    # print("image:",image)
                    messages.error(request,"Information updated successfully")
                    return redirect('vendor_settings') 
                else:
                    messages.error(request,"All fields are required")
                    return render (request, 'showout/vendor/vendor_settings.html', context) 

            else:
                return render (request, 'showout/vendor/vendor_settings.html', context) 
        except:
             messages.error(request,"Account does not xist")
             return redirect('vendor_login')


    else:
         return redirect('vendor_login')
 
# function for rendering vender add service page
def add_service(request):
    services = Services.objects.all() # fetch all services
    if 'vendor_id' in request.session: # check if the venor is loggedin
        vendorId = request.session['vendor_id'] # get vendor id from the session
        if request.method == 'POST': # check if the html form method is post
            # this block of code get the velues from the html form
            serviceId = request.POST['serviceId']
            description = request.POST['description']
            budget = request.POST['budget']
            pdfUpload = request.FILES.get('pdfUpload')
            vendor = Vendors.objects.get(pk=vendorId)
            print("vendor",vendor)
            print("vendorId",vendorId)
            service = Services.objects.get(pk=serviceId) # check if the service selected exist
            # create a new  VendorServices record in the VendorServices table 
            VendorServices.objects.create(category=service.category,vendor=vendor,services=service,description=description,budget=budget,pdfUpload=pdfUpload)
            # return success message after insertion
            messages.success(request,"Service Added successufully")
            # send email confirmation
            confirmationEmail(request,"Add Service",vendor.email)
        context = {'services':services}
        return render (request, 'showout/vendor/add_service.html', context)
    else:
        return redirect('vendor_login') 

# function for rendering vender edit service page
def edit_service(request,vendorServicesId):
    services = Services.objects.all() # fetch all services
    vendorService = VendorServices.objects.get(pk=vendorServicesId) # get a vendor service
    context = {'services':services,'vendorService':vendorService}
    if 'vendor_id' in request.session: # check if the venor is loggedin
        vendorId = request.session['vendor_id']
        if request.method == 'POST':  # check if the html form method is post

            # this block of code get the velues from the html form
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
            # update vendor service
            vendorService.save()
            # send email confirmation
            confirmationEmail(request,"Delete Service",vendorService.vendor.email)
            messages.success(request,"Service Updated successufully")
            return render (request, 'showout/vendor/vendor_edit_service.html', context)    
 
        else:
         return render (request, 'showout/vendor/vendor_edit_service.html', context)    

    else:
        return redirect('vendor_login') 

# function for rendering vender delete service page
def delete_view(request):
    if 'vendor_id' in request.session: # check if the vendor is logged in
        if request.method == 'POST': # check if the method is post
            vendorServicesId = request.GET['vendorServicesId']
            print("vendorServicesId",vendorServicesId)
            vendorService = VendorServices.objects.get(pk=vendorServicesId) # get vendor service information
            vendorService.delete()  # delete the vendor service
            confirmationEmail(request,"Delete Service",vendorService.vendor.email) # send confirmation email
            return redirect('vendor_services') 
        else:
             return redirect('vendor_services') 
    else:
        return redirect('vendor_login') 

# function for email confirmation
def confirmationEmail(request,topic,email):
    if request.method == 'POST': # check if the html form method is post
        subject = topic
        to_email =  email # Replace with the recipient's email address
        context = {'link': f'http://127.0.0.1:8000/'}
        template_path = 'showout/customers/email_template.html'
        messageString = render_to_string(template_path, context)
        from_email = 'hello@showout.studio'  # Replace with your email address
        print("to_email",to_email)   
        # create mail message 
        message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=messageString)
        try:
            # send email using send grid by passing the token
            sg = SendGridAPIClient(emailToken)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            # return to email sent page
            return redirect('emailSent')

        except Exception as e:
            print(e)
       

