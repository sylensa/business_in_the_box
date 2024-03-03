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
	countryId =  models.IntegerField(null=True,)
	genderId =  models.IntegerField(null=True,)
	
	def __str__(self):
		return self.firstName
	
    
class Category(models.Model):
	categoryName = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	categoryId = models.AutoField(primary_key=True,)
	def __str__(self):
		return self.categoryName
	


class Image(models.Model):
    image = models.ImageField(upload_to='images/')



class Services(models.Model):
	Category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)
	serviceName=models.CharField(max_length=200,null=True)
	description = models.CharField(max_lenght=200)
	date_created = models.DateTimeField(auto_now_add=True)
	serviced = models.AutoField(primary_key=True)
	image = models.ImageField(null=True, blank=True)

	def _str_(self):
		return self.serviceName
	
	@property
	def imageURL(self):
		try:
			url=self.image.url
		except:
			url=''
		return url
	
	class VendorServices(models.Model):
		vendor = models.ForeignKey(Vendors, on_delete = models.SET_NULL, null=True, blank=True)
		category = models.ForeignKey(Category, on_delete = models.SET_NULL, null=True, blank=True)
		services=models.ForeignKey(Services, on_delete = models.Set_NULL, null=True, blank=True)
		rating = models.IntegerField(primary_key=False, default=0)
		date_created = models.DateTimeField(auto_now_add=True)
		vendorServicesId= models.AutoField(primary_key=True)
		def _int_(self):
			return self.vendorServicesId
	
	



