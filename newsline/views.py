from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from newsline.forms import AddPostForm, UploadFileForm
from newsline.models import Post, Category, TagPost, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# def index(request):
#     posts = Post.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'newsline/index.html', context=data)


class Home(ListView):
    # model = Post
    template_name = 'newsline/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Post.published.all().select_related('cat')


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'newsline/about.html',
                  {"title": 'О сайте', 'menu': menu, 'form': form})


# def show_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'newsline/post.html', data)


class ShowPost(DetailView):
    model = Post
    template_name = 'newsline/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])

# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Post.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Категория: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'newsline/index.html', context=data)


class PostCategory(ListView):
    template_name = 'newsline/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


def login(request):
    return HttpResponse('Войти')


def contact(request):
    return HttpResponse('Обратная связь')


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #    Post.objects.create(**form.cleaned_data)
#             #    return redirect('home')
#             # except:
#             #    form.add_error(None, 'Ошибка добавления записи')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'newsline/addpage.html', data)


class AddPost(View):  # заменяю функцию представления на класс
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'newsline/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'newsline/addpage.html', data)


# Create your views here.
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Post.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'newsline/index.html', context=data)


class TagPostList(ListView):
    template_name = 'newsline/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
