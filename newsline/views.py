from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'newsline/index.html', context=data)


def about(request):
    return render(request, 'newsline/about.html')


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id={post_id}')


def login(request):
    return HttpResponse('Войти')


def contact(request):
    return HttpResponse('Обратная связь')


def addpage(request):
    return HttpResponse('Добавить статью')


# Create your views here.
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
