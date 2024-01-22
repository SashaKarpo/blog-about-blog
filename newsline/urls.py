from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<int:post_id>', views.show_post, name="post"),
    path('addpage/', views.addpage, name='add_page'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
