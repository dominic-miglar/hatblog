from django.views.generic import TemplateView, FormView, ListView, RedirectView, DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from hatblog.gallery.forms import CommentForm, ContactForm
from hatblog.gallery.models import Image, Category, Comment, Tag
from hatblog.weblog.tasks import jabber_notify, send_email

# Modify generic views to work with the gallery.

class GalleryFormView(FormView):
    def get_context_data(self, **kwargs):
        context = super(GalleryFormView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['lastimages'] = Image.objects.all().order_by('-dateCreated')[:5]
        context['tags'] = Tag.objects.all()
        return context


class GalleryTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(GalleryTemplateView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['lastimages'] = Image.objects.all().order_by('-dateCreated')[:5]
        context['tags'] = Tag.objects.all()
        return context


class GalleryImageView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(GalleryImageView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['lastimages'] = Image.objects.all().order_by('-dateCreated')[:5]
        context['tags'] = Tag.objects.all()
        return context


class GalleryListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['lastimages'] = Image.objects.all().order_by('-dateCreated')[:5]
        context['tags'] = Tag.objects.all()
        context['category_active'] = self.request.GET.get('category', False)
        return context



class LogoutView(RedirectView):
    permanent = False
    
    def get_redirect_url(self):
        logout(self.request)
        return reverse('gallery:images')


class ImprintView(GalleryTemplateView):
    template_name = 'gallery/imprint.html'


class ContactView(GalleryFormView):
    form_class = ContactForm
    template_name = 'gallery/contact.html' 

    def form_valid(selfs, form):
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

class ImageListView(GalleryListView):
    template_name = 'gallery/gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        tag = self.request.GET.get('tag', False)
        category = self.request.GET.get('category', False)

        if category and tag:
            images = Image.objects.filter(category__name=category, tags__name=tag)
        elif category:
            images = Image.objects.filter(category__name=category)
        elif tag:
            images = Image.objects.filter(tags__name=tag)
        else:
            images = Image.objects.all()

        images = images.order_by('-dateCreated')
        return images


class ImageView(GalleryImageView):
    template_name = 'gallery/image.html'
    model = Image
    context_object_name = 'image'
	
    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(image=self.object)
        return context
        # TODO: add comment form and so on....







