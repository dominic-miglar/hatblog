# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'weblog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('isMainCategory', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'weblog', ['Category'])

        # Adding model 'BlogEntry'
        db.create_table(u'weblog_blogentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weblog.Category'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('dateCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dateModified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'weblog', ['BlogEntry'])

        # Adding model 'Comment'
        db.create_table(u'weblog_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blogEntry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weblog.BlogEntry'])),
            ('dateCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('isApproved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'weblog', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'weblog_category')

        # Deleting model 'BlogEntry'
        db.delete_table(u'weblog_blogentry')

        # Deleting model 'Comment'
        db.delete_table(u'weblog_comment')


    models = {
        u'weblog.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weblog.Category']"}),
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'weblog.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isMainCategory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'weblog.comment': {
            'Meta': {'object_name': 'Comment'},
            'blogEntry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weblog.BlogEntry']"}),
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isApproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['weblog']