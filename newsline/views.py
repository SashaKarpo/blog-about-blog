from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from newsline.forms import AddPostForm, UploadFileForm
from newsline.models import Post, Category, TagPost, UploadFiles
from newsline.utils import DataMixin


class Home(DataMixin, ListView):
    # model = Post
    template_name = 'newsline/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all().select_related('cat')


def about(request):
    contact_list = Post.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'newsline/about.html',
                  {"title": 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'newsline/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])


class PostCategory(DataMixin, ListView):
    template_name = 'newsline/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


def login(request):
    return HttpResponse('Войти')


def contact(request):
    return HttpResponse('Обратная связь')


class AddPost(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'newsline/addpage.html'
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'newsline/addpage.html'
    title_page = 'Редактирование статьи'
    success_url = reverse_lazy('home')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class TagPostList(DataMixin, ListView):
    template_name = 'newsline/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
