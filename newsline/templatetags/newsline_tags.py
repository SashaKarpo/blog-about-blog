from django import template
import newsline.views as views
from newsline.models import Category

register = template.Library()


@register.inclusion_tag('newsline/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
