#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms

class CommentForm(forms.Form):
	name = forms.CharField(max_length=100, error_messages={'required': 'Please enter your name. This field is required.'})
	email = forms.EmailField(max_length=75, error_messages={'required': 'Please enter your email address. This field is required.'})
	subject = forms.CharField(max_length=100, error_messages={'required': 'Please enter the subject of the comment. This field is required.'})
	text = forms.CharField(widget=forms.Textarea, error_messages={'required': 'Please enter your comment text. This field is required.'})

class ContactForm(forms.Form):
	name = forms.CharField(max_length=100, error_messages={'required': 'Please enter your name. This field is required.'})
	email = forms.EmailField(max_length=100, error_messages={'required': 'Please enter your email address. This field is required.'})
	subject = forms.CharField(max_length=100, error_messages={'required': 'Please enter the subject. It should contain a few keywords of why you are contacting me. This field is required.'})
	text = forms.CharField(widget=forms.Textarea, error_messages={'required': 'Please enter your matter. This field is required.'})
	cc_myself = forms.BooleanField(label='CC myself', required=False)
	