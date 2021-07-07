from django.db import models
from django.db.models.base import Model
# from django.db.models.fields import DateTime

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()