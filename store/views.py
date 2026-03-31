from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product
from category.models import Category 
from carts.views import _cart_id, CartItem
from carts.models import CartItem

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        products_count = products.count()

    context = {
        'products' : products,
        'products_count' : products_count ,
    }
    return render(request,'store/store.html', context )

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    # Handle "Mua vé" form submission: redirect to add_cart with price as GET param
    price = request.GET.get('price')
    if price:
        add_url = reverse('add_cart', args=[single_product.id])
        return redirect(f"{add_url}?price={price}")

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)
