from django.shortcuts import render
from blog.models import Post,Tag

# All Posts View
def blog(request):
    posts = Post.objects.all()
    return render(request, 'blog/blog.html', context={'posts':posts})

# Post Detail View
def postdetail(request, slug):
    post = Post.objects.get(slug__iexact=slug)
    return render(request, 'blog/postdetail.html', context={'post':post})

# All Tags View
def alltags(request):
    tags = Tag.objects.all()
    return render(request, 'blog/alltags.html', context={'tags':tags})

# Tag Detail View
def tagdetail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'blog/tagdetail.html', context={'tag':tag})