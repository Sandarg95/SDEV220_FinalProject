from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    food_items = models.ManyToManyField(FoodItem)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

    def total_price(self):
        """Calculates total price of the order."""
        return sum(food_item.price for food_item in self.food_items.all())