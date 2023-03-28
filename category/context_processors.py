from category.models import Category

# Custom Link For Showing Categories !
def menu_links(request):
    links= Category.objects.all()
    context={
        'links':links,
    }
    return context