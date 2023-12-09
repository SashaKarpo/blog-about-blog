from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    return HttpResponse('Cnhfyb')


def post(request):
    return HttpResponse('post')


def archive(request, year):
    if year > 2023:
        return redirect('home', permanent=True)

    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


# Create your views here.
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
