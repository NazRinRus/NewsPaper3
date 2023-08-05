from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
   path('', PostList.as_view(), name = 'posts_all'),
   path('<int:pk>/', PostDetail.as_view(), name = 'post_id'),
   path('news/', PostListNews.as_view(), name = 'news_all'),
   path('articles/', PostListArticles.as_view(), name = 'articles_all'),
   path('news/<int:pk>/', PostDetailNews.as_view(), name = 'news_id'),
   path('articles/<int:pk>/', PostDetailArticles.as_view(), name='articles_id'),
   path('news/search', NewsSearch.as_view(), name = 'search_form'),
   path('articles/search', ArticlesSearch.as_view(), name='articles_search_form'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('about/', about, name='about'),
   path('contact/', contact, name='contact'),
   path('sign/', include('sign.urls')),
]