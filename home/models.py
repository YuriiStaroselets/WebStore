from django.db import models
from store.models import Product


class Awesome(models.Model):
    product = models.OneToOneField(Product,  on_delete=models.CASCADE)
    is_awesome = models.BooleanField(default=False)
