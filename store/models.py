from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from category.models import Category
from django.urls import reverse

# Default price tiers applied automatically to every new product
DEFAULT_PRICE_TIERS = ['200000', '500000', '1000000', '1500000', '2000000']

# Create your models here.

class Product(models.Model):
    product_name  = models.CharField(max_length=200, unique=True)
    slug          = models.SlugField(max_length=200, unique=True)
    description   = models.TextField(max_length=500, blank=True)
    price         = models.IntegerField()
    images        = models.ImageField(upload_to='photos/products')
    event_date    = models.CharField(max_length=50, blank=True, default='')
    event_time    = models.CharField(max_length=50, blank=True, default='')
    venue         = models.CharField(max_length=200, blank=True, default='')
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def get_min_ticket_price(self):
        prices = []
        for value in self.variation_set.prices().values_list('variation_value', flat=True):
            try:
                prices.append(int(value))
            except (TypeError, ValueError):
                continue

        return min(prices) if prices else self.price

class VariationManager(models.Manager):
    def prices(self):
        return super(VariationManager, self).filter(variation_category='price', is_active=True)


class Variation(models.Model):

    variation_category_choice = (
        ('price', 'price'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


@receiver(post_save, sender=Product)
def create_default_variations(sender, instance, created, **kwargs):
    """Automatically add default price variations when a new Product is created."""
    if created:
        for price in DEFAULT_PRICE_TIERS:
            Variation.objects.get_or_create(
                product=instance,
                variation_category='price',
                variation_value=price,
                defaults={'is_active': True},
            )