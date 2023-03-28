from django.contrib import admin
from store.models import Product

# Registering Product Model Admin !
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','price','stock','is_available','category','modified_date')

admin.site.register(Product, ProductAdmin)
