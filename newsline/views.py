from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string


def index(request):
    # item = render_to_string('newsline/index.html')
    return render(request, 'newsline/index.html')


def about(request):
    return render(request, 'newsline/about.html')


def post(request):
    return HttpResponse('post')


def archive(request, year):
    if year > 2023:
        return redirect('home', permanent=True)

    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


# Create your views here.
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
