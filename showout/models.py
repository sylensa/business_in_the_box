from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Country(models.Model):
	countryName = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.countryName
	
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	firstName = models.CharField(max_length=200, null=True)
	lastName = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	buget = models.CharField(max_length=200)
	country =  models.OneToOneField(Country, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.firstName
	
    
class Vendors(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	vendorName = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	country =  models.OneToOneField(Country, null=True, blank=True, on_delete=models.CASCADE)
	aboout = models.CharField(max_length=200)
	website = models.CharField(max_length=200)
	facebook = models.CharField(max_length=200)
	twitter = models.CharField(max_length=200)
	linkedIn = models.CharField(max_length=200)
	tiktok = models.CharField(max_length=200)
	instagram = models.CharField(max_length=200)

	def __str__(self):
		return self.vendorName
	

class Category(models.Model):
	categoryName = models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.categoryName
	
class VendorServices(models.Model):
	vendor = models.OneToOneField(Vendors, null=True, blank=True, on_delete=models.CASCADE)
	category = models.OneToOneField(Category, null=True, blank=True, on_delete=models.CASCADE)
	serviceName = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.serviceName
	

class Services(models.Model):
	category = models.OneToOneField(Category, null=True, blank=True, on_delete=models.CASCADE)
	serviceName = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200)
	def __str__(self):
		return self.serviceName	

	
	
class WishList(models.Model):
	vendor = models.OneToOneField(Vendors, null=True, blank=True, on_delete=models.CASCADE)
	service = models.OneToOneField(Services, null=True, blank=True, on_delete=models.CASCADE)
	customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.serviceName
	


