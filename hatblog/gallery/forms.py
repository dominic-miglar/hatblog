#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from hatblog.gallery.models import Comment

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'email', 'subject', 'text']

class ContactForm(forms.Form):
	name = forms.CharField(max_length=100, error_messages={'required': 'Please enter your name. This field is required.'})
	email = forms.EmailField(max_length=100, error_messages={'required': 'Please enter your email address. This field is required.'})
	subject = forms.CharField(max_length=100, error_messages={'required': 'Please enter the subject. It should contain a few keywords of why you are contacting me. This field is required.'})
	text = forms.CharField(widget=forms.Textarea, error_messages={'required': 'Please enter your matter. This field is required.'})
	cc_myself = forms.BooleanField(label='CC myself', required=False)
	