#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime

from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from hatblog.weblog.models import BlogEntry, Category, Comment
from hatblog.weblog.forms import CommentForm, ContactForm

from hatblog.weblog.tasks import jabber_notify, send_email

def categories():
    main_categories = Category.objects.filter(isMainCategory=True)
    categories = Category.objects.all()
    ctx = {
        "main_categories": main_categories,
        "categories": categories
    }
    return ctx

def latest_blog_entries():
    entries = BlogEntry.objects.all()
    entries = entries.order_by('-dateCreated')[:5]
    ctx = {
        "latest_blog_entries": entries
    }
    return ctx


def home(request):
    try:   
        category = request.GET['category']
    except MultiValueDictKeyError:
        category = None
        
    if category:
            category = get_object_or_404(Category, name=category)
            blogentries = BlogEntry.objects.filter(category__name=category.name)
            category_description = Category.objects.filter(name=category)[0].description
            category = category.name # vorbereitung fuer category_active im ctx
    else:
        blogentries = BlogEntry.objects.filter()
        category_description = None

    blogentries = blogentries.order_by('-dateCreated')

    ctx = {
        'entries': blogentries, 
        'category_active': category,
        'category_description': category_description,
        }
    ctx.update(categories())
    ctx.update(latest_blog_entries())
    return render(request, 'weblog/blog.html', ctx)


def archive(request, year=None, month=None, day=None):
    """Renders the archive of a day/month/year.

    If a category is given with a GET parameter, only the 
    BlogEntries of the given category are given to the template

    """

    try:
        category = request.GET['category']
        category_description = Category.objects.filter(name=category)[0].description
    except MultiValueDictKeyError:
        category = None
        category_description = None

    if day:
        if category:
            blogentries = BlogEntry.objects.filter(
                dateCreated__year=year, 
                dateCreated__month=month, 
                dateCreated__day=day, 
                category=category)
        else:
            blogentries = BlogEntry.objects.filter(
                dateCreated__year=year,
                dateCreated__month=month,
                dateCreated__day=day)
    elif month:
        if category:
            blogenties = BlogEntry.objects.filter(
                dateCreated__year=year,
                dateCreated__month=month,
                category=category)
        else:
            blogentries = BlogEntry.objects.filter(
                dateCreated__year=year,
                dateCreated__month=month)
    elif year:
        if category:
            blogentries = BlogEntry.objects.filter(
                dateCreated__year=year,
                category=category)
        else:
            blogentries = BlogEntry.objects.filter(
                dateCreated__year=year)

    blogentries = blogentries.order_by('-dateCreated')
    
    ctx = {
        'category_description': category_description,
        'entries': blogentries,
        'category_active': category
    }
    ctx.update(categories()) 
    ctx.update(latest_blog_entries())
    return render(request, 'weblog/blog.html', ctx)


def blogentry_detail(request, year=None, month=None, day=None, id=None, slug=None):
    entry = BlogEntry.objects.filter(pk=id)
    entry = entry[0]
    comments = Comment.objects.filter(blogEntry__pk=id, isApproved=True)
    commented = False


    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.blogEntry = entry
            comment.dateCreated = datetime.now()
            comment.isApproved = False
            comment.name = form.cleaned_data['name']
            comment.email = form.cleaned_data['email']
            comment.subject = form.cleaned_data['subject']
            comment.text = form.cleaned_data['text']
            comment.save()
            commented = True
            notify_message = u'Hello! A new comment was submitted on hatblog. Details below.\n\nFrom: {}\nE-Mail: {}\n\nBelongs to blog entry: {}\nSubject: {}\n\n{}'.format(
                comment.name, comment.email, comment.blogEntry.subject, comment.subject, comment.text) 
            send_email.delay(subject='[hatblog] new comment', text=notify_message)
            jabber_notify.delay(notify_message)

    else:
        form = CommentForm()

    if commented:
        form = CommentForm()

    ctx = {
        'commented': commented, # is true if the user just commented the article
        'form': form,
        'entry': entry, 
        'comments': comments,
    }
    ctx.update(categories())
    ctx.update(latest_blog_entries())
    return render(request, 'weblog/blogentry_detail.html', ctx)


def imprint(request):
    ctx = categories() 
    ctx.update(latest_blog_entries())
    return render(request, 'weblog/imprint.html', ctx)


def contact(request):
    contacted = False

    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['cc_myself']:
                send_email.delay(
                    subject=form.cleaned_data['subject'], 
                    text=form.cleaned_data['text'], 
                    cc=form.cleaned_data['email'],
                    reply_to=form.cleaned_data['email']
                    )
            else:
                send_email.delay(
                    subject=form.cleaned_data['subject'], 
                    text=form.cleaned_data['text'],
                    reply_to=form.cleaned_data['email']
                    )
            contacted = True
    else:
        form = ContactForm()

    ctx = {
        'contacted': contacted, # is true if the user just (valid) filled out the contactform
        'form': form,
    }
    ctx.update(categories())
    ctx.update(latest_blog_entries())
    return render(request, 'weblog/contact.html', ctx)

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return redirect('/blog/')
