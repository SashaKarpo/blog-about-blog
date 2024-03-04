from django import forms
from .models import Husband, Category


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label='Slug')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows':5}), label='Содержимое')
    is_published = forms.BooleanField(required=False, label='Опубликовать?', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Не замужем')
