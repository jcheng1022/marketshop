from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES = (
    ('E','Electronics'),
    ('T','Toys'),
    ('H', 'Home Decor'),
    ('B', 'Beauty'),
    ('S', 'Sport Items'),
    ('O', 'Office Items'),
    ('X', 'Other')
)

class Item(models.Model):
    name = models.CharField(max_length = 100)
    category = models.CharField(
        max_length = 1,
        default = CATEGORIES[6][0]
    )
    price = models.IntegerField()
    description = models.TextField(max_length = 350)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.name
