from django.db import models
from vendor.models import Vendor
# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique= True)
    description = models.TextField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self) -> str:
        return self.category_name


class Fooditem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="fooditems")
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.food_title

