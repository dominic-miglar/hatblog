from django.contrib import admin
from hatblog.gallery.models import Image, Category, Comment, Tag


admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)

