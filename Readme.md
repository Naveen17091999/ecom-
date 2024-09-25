# Set Up Django Project

 1. django-admin startproject ecommerce
 2. cd ecommerce
 3. django-admin startapp shop

# Install Required Packages

 1. pip install djangorestframework
 2. pip install djangorestframework-simplejwt
 3. pip install django-cors-headers
4. pip install mysqlclient


# Enable Models in Admin Panel

from django.contrib import admin  
from .models import Category, SubCategory, Product  

admin.site.register(Category)  
admin.site.register(SubCategory)  
admin.site.register(Product)