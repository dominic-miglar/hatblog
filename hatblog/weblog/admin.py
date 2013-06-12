#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from hatblog.weblog.models import Category, BlogEntry, Comment


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'isMainCategory', 'description')
	fieldsets = [
		('General', {'fields': ['name', 'isMainCategory']}),
		('Description', {'fields': ['description']}),
	]

class CommentAdmin(admin.ModelAdmin):
	list_display = ('subject', 'blogEntry', 'dateCreated', 'isApproved')
	fieldsets = [
		('General', {'fields': ['blogEntry', 'isApproved']}),
		('Date information', {'fields': ['dateCreated']}),
		('Personal information', {'fields': ['name', 'email']}),
		('Comment information', {'fields': ['subject', 'text']}),
	]
	readonly_fields = ('dateCreated',)

class BlogEntryAdmin(admin.ModelAdmin):
	list_display = ('subject', 'category', 'dateCreated', 'dateModified')
	fieldsets = [
		('General', {'fields': ['category']}),
		('Date information', {'fields': ['dateCreated', 'dateModified']}),
		('Blog Entry', {'fields': ['subject', 'slug', 'text']}),
	]
	readonly_fields = ('dateCreated', 'dateModified', )

	class Media:
   		js = [
        	'/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        	'/static/grappelli/tinymce_setup/tinymce_setup.js',
    	]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BlogEntry, BlogEntryAdmin)
