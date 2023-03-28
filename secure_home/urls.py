from django.contrib import admin
from django.urls import path,include
from . import views

# Media File Configuration !
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    
    path("accounts/", include('accounts.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('blog/', include('blog.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
