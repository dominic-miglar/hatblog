#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from markdown import markdown


class Category(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True)
    isMainCategory = models.BooleanField()

    class Meta:
    	verbose_name = 'Category'
    	verbose_name_plural = 'Categories'

    def __unicode__(self):
    	return self.name



class BlogEntry(models.Model):
    category = models.ForeignKey(Category, verbose_name='Category')
    subject = models.CharField('Subject', max_length=100)
    slug = models.SlugField()
    text = models.TextField('Text')
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    @property
    def text_to_html(self):
        return markdown(self.text, extensions=['codehilite(linenums=True)'])

    def __unicode__(self):
        return self.subject



class Comment(models.Model):
    blogEntry = models.ForeignKey(BlogEntry)
    dateCreated = models.DateTimeField(auto_now_add=True)
    isApproved = models.BooleanField()
    name = models.CharField('Name', max_length=100)
    email = models.EmailField('E-Mail', max_length=75)
    subject = models.CharField('Subject', max_length=100)
    text = models.TextField('Text')

    class Meta:
    	verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __unicode__(self):
    	return self.subject
