from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Husband, Category
from django.core.validators import MinLengthValidator, MaxLengthValidator


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только руские буквы, цифры, дефис или пробел'

    def __call__(self, values, *args, **kwargs):
        if not (set(values) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Слишком короткое',
                                'required': 'Без заголовка никак',
                            })
    slug = forms.SlugField(max_length=255, label='Slug',
                           validators=[
                               MinLengthValidator(5),
                               MaxLengthValidator(255),
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label='Содержимое')
    is_published = forms.BooleanField(required=False, label='Опубликовать?', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж',
                                     empty_label='Не замужем')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только руские буквы, цифры, дефис или пробел')
