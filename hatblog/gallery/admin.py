#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from hatblog.gallery.models import Image, Category, Comment, Tag

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'isMainCategory', 'description')
	fieldsets = [
		('General', {'fields': ['name', 'isMainCategory']}),
		('Description', {'fields': ['description']}),
	]

class ImageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'dateCreated')
	fieldsets = [
		('General', {'fields': ['title', 'slug', 'category']}),
		('Time information', {'fields': ['dateCreated']}),
		('Image', {'fields': ['image']}),
		('Tags', {'fields': ['tags']}),
	]
	readonly_fields = ('dateCreated',)
	filter_horizontal = ('tags',)


admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
