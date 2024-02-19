from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Country(models.Model):
	countryName = models.CharField(max_length=200, null=True)
	countryId =  models.IntegerField(primary_key=True,default=1)
	def __str__(self):
		return self.countryName
	
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
	customerId =  models.IntegerField(primary_key=True,default=1)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
	

	def __str__(self):
		return self.firstName
	
    
class Vendors(models.Model):
	vendorName = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
	aboout = models.CharField(max_length=200)
	website = models.CharField(max_length=200)
	facebook = models.CharField(max_length=200)
	twitter = models.CharField(max_length=200)
	linkedIn = models.CharField(max_length=200)
	tiktok = models.CharField(max_length=200)
	instagram = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	approved = models.BooleanField(default=False)
	vendorId =  models.IntegerField(primary_key=True,default=1)

	def __str__(self):
		return self.vendorName
	

class Category(models.Model):
	categoryName = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	categoryId = models.IntegerField(primary_key=True,default=1)
	def __str__(self):
		return self.categoryName
	

	

class Services(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	serviceName = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	serviceId = models.IntegerField(primary_key=True,default=1)
	def __str__(self):
		return self.serviceName	

	
class VendorServices(models.Model):
	vendor = models.OneToOneField(Vendors, null=True, blank=True, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	services = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	vendorServicesId =  models.IntegerField(primary_key=True,default=1)
	def __str__(self):
		return self.vendor.vendorName	
class WishList(models.Model):
	vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True, blank=True)
	service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	wishListId =  models.IntegerField(primary_key=True,default=1)

	def __str__(self):
		return self.service.serviceName
	


