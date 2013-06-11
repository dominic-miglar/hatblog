#!/usr/bin/env python
#-*- coding:utf-8 -*-

from os.path import dirname, abspath, join


# Shortcut for the environment directory
ENV_ROOT = dirname(dirname(dirname(abspath(__file__))))

DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE

ALLOWED_HOSTS = '*'
ADMINS = (
    # ('Firehat', 'firehat@w1r3.net'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'firehat_firehat.w1r3.org',
        'USER': 'firehat',
        'PASSWORD': '_f1r3f0rw1r31ny0urf4c3_',
        'HOST': 'yuri.munich.w1r3.net',
        'PORT': '',  # Set to empty string for default.
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(ENV_ROOT, 'files/firehat.w1r3.org/upload/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(ENV_ROOT, 'files/firehat.w1r3.org/static/')
SECRET_KEY = 'c3b2440d29274eb98ed86694e9f250c8652fdf12da6740dc87dda94ce3342e63'
