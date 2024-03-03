from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from pathlib import Path

# Create your models here.
from django.core.files.storage import FileSystemStorage
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
fs = FileSystemStorage(location=MEDIA_ROOT)

class Country(models.Model):
	countryName = models.CharField(max_length=200, null=True)
	countryId =  models.AutoField(primary_key=True)
	def __str__(self):
		return self.countryName
	

class Gender(models.Model):
	genderName = models.CharField(max_length=200, null=True)
	genderId =  models.AutoField(primary_key=True)
	def __str__(self):
		return self.genderName
	
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	firstName = models.CharField(max_length=200, null=True)
	lastName = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	mobile = models.CharField(max_length=200, null=True)
	password = models.CharField(max_length=200)
	buget = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True,null=True,)
	customerId =  models.AutoField(primary_key=True,)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
	

	def __str__(self):
		return self.firstName
	
    


	def __str__(self):
		return self.vendorName
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	

class Category(models.Model):
	categoryName = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	categoryId = models.AutoField(primary_key=True,)
	def __str__(self):
		return self.categoryName
	

	
class ReviewVendorServices(models.Model): 
	vendor = models.Foreignkey(Vendors, on_delete=models.SET_NULL, null=True, blank=True) 
	vendorService = models.Foreignkey(VendorServices, ondelete=models.SET.NULL, null=True, blank=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	reviewVendoreservicesId=models.AutoField(primary_key=True) 
	vendorServicesId= models.IntegerField(primary_key=False,)	
	rating = models.FloatField(primary_key=Fals)
	review= models.CharField(max_length=500)
	def _init_(self): 	
		return self.reviewVendoreServicesId	
	
class WishList(models.Model):
	vendor = models.ForeignKey(Vendors,  on_delete=models.SET_NULL, null=True, blank=True)
	vendorService = models.ForeignKey(VendorServices,  on_delete=models.SET_NULL, null=True, blank=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	wishListId =  models.AutoField(primary_key=True)

	def __str__(self):
		return self.vendorService.services.serviceName
	


class Image(models.Model):
    image = models.ImageField(upload_to='images/')