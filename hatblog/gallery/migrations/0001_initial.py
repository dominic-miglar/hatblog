# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'gallery_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('isMainCategory', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'gallery', ['Category'])

        # Adding model 'Tag'
        db.create_table(u'gallery_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'gallery', ['Tag'])

        # Adding model 'Image'
        db.create_table(u'gallery_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Category'])),
            ('dateCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'gallery', ['Image'])

        # Adding M2M table for field tags on 'Image'
        m2m_table_name = db.shorten_name(u'gallery_image_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm[u'gallery.image'], null=False)),
            ('tag', models.ForeignKey(orm[u'gallery.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['image_id', 'tag_id'])

        # Adding model 'Comment'
        db.create_table(u'gallery_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Image'])),
            ('dateCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('isApproved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'gallery', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'gallery_category')

        # Deleting model 'Tag'
        db.delete_table(u'gallery_tag')

        # Deleting model 'Image'
        db.delete_table(u'gallery_image')

        # Removing M2M table for field tags on 'Image'
        db.delete_table(db.shorten_name(u'gallery_image_tags'))

        # Deleting model 'Comment'
        db.delete_table(u'gallery_comment')


    models = {
        u'gallery.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isMainCategory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'gallery.comment': {
            'Meta': {'object_name': 'Comment'},
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gallery.Image']"}),
            'isApproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'gallery.image': {
            'Meta': {'object_name': 'Image'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gallery.Category']"}),
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gallery.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gallery.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['gallery']