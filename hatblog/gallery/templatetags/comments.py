from django import template

register = template.Library()

@register.inclusion_tag('gallery/image_comments.html')
def image_show_comments(image):
    image_comments = image.get_comments()
    image_comments = image_comments.filter(isApproved=True)
    return {'object_list': image_comments}