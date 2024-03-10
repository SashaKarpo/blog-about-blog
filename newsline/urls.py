from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name="post"),
    path('addpage/', views.AddPost.as_view(), name='add_page'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('category/<slug:cat_slug>/', views.PostCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
]
