from store.models import Product
from category.models import Category
from django.shortcuts import render,get_object_or_404,HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from carts.models import Cart,CartItem
from carts.views import _cart_id

# Store View Functionality !
def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories =get_object_or_404(Category, slug=category_slug)
        products =Product.objects.filter(category=categories, is_available=True).order_by('id')
        product_count=products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        product_count=products.count()
    
    context={
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)

# Product Detail Functionality !
def product_detail(request, product_slug, category_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
       
    except Exception as e:
        raise e
    
    context={
        'single_product' : single_product,
        'in_cart' : in_cart,
    }
    return render(request, 'store/productdetail.html', context)

# Search Functionality !
def search(request):
    if 'q' in request.GET:
        q=request.GET['q']
        if q:
            products=Product.objects.filter(Q(description__icontains=q)|Q(product_name__icontains=q)).order_by('-created_date')
            product_count=products.count()
    context={
        'products': products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)