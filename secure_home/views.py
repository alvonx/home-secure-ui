from django.shortcuts import render
from store.models import Product
from blog.models import Post

# Home Functionality !
def home(request):
    posts = Post.objects.all()
    products = Product.objects.all().filter(is_available=True)

    context={
        'products':products,
        'posts':posts,
    }
    return render (request,'secure_home/home.html', context)

# About Us Functionality !
def about(request):
    return render (request, 'secure_home/about.html')

# Service Functionality !
def service(request):
    return render (request, 'secure_home/services.html')