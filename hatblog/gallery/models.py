from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from hatblog.settings import THUMB_MAX_SIZE_HEIGHT, THUMB_MAX_SIZE_WIDTH, MEDIA_ROOT, MEDIA_URL
from cStringIO import StringIO
import PIL
import os


class Category(models.Model):
    name = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    isMainCategory = models.BooleanField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __unicode__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(Category)
    dateCreated = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='gallery/images/')
    thumbnail = models.ImageField(upload_to='gallery/thumbs/', null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def create_thumbnail(self):
        if not self.image:
            return

        fileName, fileExtension = os.path.splitext(self.image.path)
        fileExtension = fileExtension.lower()
        fileExtension = fileExtension.split('.')[1]

        if fileExtension == 'jpg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        else:
            PIL_TYPE = fileExtension
            FILE_EXTENSION = fileExtension

        image = PIL.Image.open(StringIO(self.image.read()))
        image.thumbnail((THUMB_MAX_SIZE_WIDTH, THUMB_MAX_SIZE_HEIGHT), PIL.Image.ANTIALIAS)
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read())
        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    def save(self):
        self.create_thumbnail()
        super(Image, self).save()

    def delete(self):
        try:
            self.image.delete(save=False)
            self.thumbnail.delete(save=False)
            super(Image, self).delete()
        except OSError:
            print "could not delete %s" % self.file.path

    def __unicode__(self):
        return os.path.basename(self.image.path)


class Comment(models.Model):
    image = models.ForeignKey(Image)
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

