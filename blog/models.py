from django.db import models
from django.shortcuts import reverse
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    image = models.ImageField(upload_to="blogpost/")
    slug = models.SlugField(max_length=150, unique=True)
    body = RichTextUploadingField()
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("postdetail", kwargs={"slug": self.slug})
    
# Tag Model
class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to="tags/")

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.image.url))

    def get_absolute_url(self):
        return reverse("tagdetail", kwargs={"slug": self.slug})