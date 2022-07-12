from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

# Create your models here.

CATEGORIES = (
    ('E','Electronics'),
    ('T','Toys'),
    ('H', 'Home Decor'),
    ('B', 'Beauty'),
    ('S', 'Sport Items'),
    ('O', 'Office Items'),
    ('O', 'Other')
)

class Item(models.Model):
    name = models.CharField(max_length = 100)
    category = models.CharField(
        max_length = 15,
        choices = CATEGORIES,
        default = CATEGORIES[6][0]
    )
    price = models.IntegerField()
    description = models.TextField(max_length = 350)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'item_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length = 200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for item_id: {self.item_id} @ {self.url}"