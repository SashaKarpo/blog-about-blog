from django.urls import path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('post/', views.post),
    path('archive/<year4:year>/', views.archive),
]
