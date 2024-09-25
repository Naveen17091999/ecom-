from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('SELLER', 'Seller'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='USER')


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'SELLER'})

    def __str__(self):
        return self.name

# Cart and Order
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)