from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('page/<int:page_number>/', views.main, name='main_pagination'),
    path('add_author/', views.add_author, name='add_author'),
    path('author/<str:fullname>/', views.about, name='about'),    
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('tag/<str:tag>/', views.view_tag, name='tag'),
    path('tag/<str:tag>/page/<int:page_number>/', views.view_tag, name='tag_pagination'),
    path('scraping/', views.scraping, name='scraping'),
    path('my-quotes/', views.view_my_quotes, name='my-quotes'),
    path('my-tags/', views.view_my_tags, name='my-tags'),
    path('my-authors/', views.view_my_authors, name='my-authors'),
    path('delete-author/<str:fullname>/', views.delete_author, name='delete_author'),
    path('delete-tag/<str:tag>/', views.delete_tag, name='delete_tag'),
    path('delete-quote/<int:quote_id>/', views.delete_quote, name='delete_quote'),
]