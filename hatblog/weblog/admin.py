#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from hatblog.weblog.models import Category, BlogEntry, Comment

admin.site.register(Category)
admin.site.register(BlogEntry)
admin.site.register(Comment)
