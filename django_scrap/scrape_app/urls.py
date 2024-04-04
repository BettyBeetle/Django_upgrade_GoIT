from django.urls import path
from . import views
from . import utils
app_name = 'scrape_app'

urlpatterns = [
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author_detail/<int:author_id>/', views.author_detail, name='author_detail'),
    path('quote_detail/<int:quote_id>/', views.quote_detail, name='quote_detail'),
    path('authors_list_db/', views.authors_list_db, name='authors_list_db'),
    path('quotes_list_db/', views.quotes_list_db, name='quotes_list_db'),
    path('quotes_www/', views.quotes_www, name='quotes_www'),
    path('about_authors/', utils.about_authors, name='about_authors'),
    path('scrape/quotes/', utils.scrape_quotes, name='scrape_quotes'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
]


