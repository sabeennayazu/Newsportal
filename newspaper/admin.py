from django.contrib import admin
from newspaper.models import Advertisement, Category, Tag, Post
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Advertisement)