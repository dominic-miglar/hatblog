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
from django.core.mail import send_mail, EmailMessage

from hatblog.weblog.models import BlogEntry, Category, Comment
from hatblog.weblog.forms import CommentForm, ContactForm
from hatblog.weblog.jabber_notify import jabber_notify


def home(request):
    """Renders the home page of the blog. Shows the latest 10 blog posts."""

    try:   
        category = request.GET['category']
    except MultiValueDictKeyError:
        category = None
        
    if category:
            category = get_object_or_404(Category, name=category)
            blogentries = BlogEntry.objects.filter(category__name=category)
            category_description = Category.objects.filter(name=category)[0].description
    else:
        blogentries = BlogEntry.objects.filter()
        category_description = None

    blogentries = blogentries.order_by('-dateCreated')

    ctx = {
        'entries': blogentries, 
        'category_active': category,
        'category_description': category_description,
        }
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
            notify_message = 'Hello! A new comment was submitted on hatblog. Details below.\n\nFrom: {}\nE-Mail: {}\n\nBelongs to blog entry: {}\nSubject: {}\n\n{}'.format(
                comment.name, comment.email, comment.blogEntry.subject, comment.subject, comment.text) 
            jabber_notify(notify_message)
            send_mail('[hatblog] New comment', notify_message, 'noreply@firehat.w1r3.org', ['firehat@w1r3.net'])

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
    return render(request, 'weblog/blogentry_detail.html', ctx)


def impressum(request):
    
    return render(request, 'weblog/impressum.html')



# TO FIX - smtp server (souo) rejected die email -
# Jun 04 12:05:05 suou postfix/smtpd[23084]: connect from mail.htl-villach.at[212.152.179.98]
# Jun 04 12:05:08 suou postfix/smtpd[23084]: NOQUEUE: reject: RCPT from mail.htl-villach.at[212.152.179.98]: 554 5.1.8 <noreply@serverkiller.net>: Sender address rejected: Domain not found; from=<...t.localdomain>
# Jun 04 12:05:08 suou postfix/smtpd[23084]: disconnect from mail.htl-villach.at[212.152.179.98]

def contact(request):
    contacted = False

    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['cc_myself']:
                email = EmailMessage(form.cleaned_data['subject'], 
                                     form.cleaned_data['text'], 
                                     'noreply@serverkiller.net',
                                     ['firehat@w1r3.net'],
                                     [form.cleaned_data['email']],
                                     headers = {'Reply-To': form.cleaned_data['email']}
                                     )
            else:
                email = EmailMessage(form.cleaned_data['subject'], 
                                     form.cleaned_data['text'], 
                                     'noreply@serverkiller.net',
                                     ['firehat@w1r3.net'],
                                     headers = {'Reply-To': form.cleaned_data['email']}
                                     )
            email.send()
            contacted = True
    else:
        form = ContactForm()

    ctx = {
        'contacted': contacted, # is true if the user just (valid) filled out the contactform
        'form': form,
    }

    return render(request, 'weblog/contact.html', ctx)
    
@login_required
def management(request):

    return render(request, 'weblog/management.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return redirect('/blog/')






