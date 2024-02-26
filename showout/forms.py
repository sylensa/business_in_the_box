from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Vendors, Customer

class VendorRegistrationForm(UserCreationForm):
    class Meta:
        model = Vendors
        fields = ['vendorName', 'email', 'password',]

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['firstName','lastName', 'email', 'password']