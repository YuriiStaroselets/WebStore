
from django.db import models
from category.models import MainCategory, SubCategory, Category, Brand
from django.urls import reverse
from accounts.models import Account


class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    product_slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    product_image = models.ImageField(upload_to='products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.main_category.slug, self.category.slug, self.sub_category.slug, self.product_slug])

    def get_total_stock(self):
        variations = Variation.objects.filter(product=self)
        total_stock = sum(variation.variation_stock for variation in variations)
        return total_stock

    def __str__(self):
        return self.product_name


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_size = models.CharField(max_length=100)
    variation_stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variation_size


class Carousel(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to='products')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BestSellers(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_best = models.BooleanField(default=False)

    def __unicode__(self):
        return self.product


class ReviewRating(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     user = models.ForeignKey(Account, on_delete=models.CASCADE)
     subject = models.CharField(max_length=100, blank=True)
     review = models.TextField()
     rating = models.FloatField()
     ip = models.CharField(max_length=20, blank=True)
     status = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
         return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', max_length=225)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
