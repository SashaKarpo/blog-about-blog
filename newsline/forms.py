from django import forms
from .models import Husband, Category


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False)
