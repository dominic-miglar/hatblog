#!/usr/bin/env python
#-*- coding:utf-8 -*-

from hatblog.weblog.models import BlogEntry, Category, Comment

def categories(request):
	main_categories = Category.objects.filter(isMainCategory=True)
	categories = Category.objects.all()
	ctx = {
		"main_categories": main_categories,
		"categories": categories
	}
	return ctx

def latest_blog_entries(request):
	entries = BlogEntry.objects.all()
	entries = entries.order_by('-dateCreated')[:5]
	ctx = {
		"latest_blog_entries": entries
	}
	return ctx