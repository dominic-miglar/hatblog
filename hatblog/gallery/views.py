from django.views.generic import TemplateView, FormView, ListView, RedirectView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.views.generic.edit import FormMixin
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


class GalleryDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
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
        return HttpResponseRedirect(reverse('gallery:contact'))

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


class ImageView(View):
    def get(self, request, *args, **kwargs):
        view = ImageViewWithComments.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ImageViewAddComment.as_view()
        return view(request, *args, **kwargs)


class ImageViewWithComments(GalleryDetailView):
    model = Image
    template_name = 'gallery/image.html'

    def get_context_data(self, **kwargs):
        context = super(ImageViewWithComments, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class ImageViewAddComment(SingleObjectMixin, GalleryFormView):
    template_name = 'gallery/image.html'
    form_class = CommentForm
    model = Image

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ImageViewAddComment, self).post(request, *args, **kwargs)

    def get_success_url(self):
        url = self.object.get_absolute_url()
        return url

    def form_valid(self, form):
        CommentObject = Comment(
            image = self.object,
            isApproved = False,
            name = form.cleaned_data['name'],
            email = form.cleaned_data['email'],
            subject = form.cleaned_data['subject'],
            text = form.cleaned_data['text']
            )
        CommentObject.save()
        notify_message = u'Hello! A new comment was submitted in the gallery. Details below.\n\nFrom: {}\nE-Mail: {}\n\nBelongs to blog entry: {}\nSubject: {}\n\n{}'.format(
                CommentObject.name, CommentObject.email, CommentObject.image.get_filename(), CommentObject.subject, CommentObject.text) 
        jabber_notify.delay(notify_message)
        return HttpResponseRedirect(self.get_success_url())





