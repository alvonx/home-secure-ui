from django.contrib import admin
from .models import Post,Tag

# Post Model Admin
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display=('id','title','date_pub')
    
admin.site.register(Post, PostAdmin)

# Tag Model Admin
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display=('id','title','slug','image_tag')
    
admin.site.register(Tag, TagAdmin)
