from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
   path('', cache_page(60*1)(PostList.as_view()), name = 'posts_all'),
   path('<int:pk>/', PostDetail.as_view(), name = 'post_id'),
   path('news/', cache_page(60*1)(PostListNews.as_view()), name = 'news_all'),
   path('articles/', cache_page(60*1)(PostListArticles.as_view()), name = 'articles_all'),
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
   path('category/', CategoryList.as_view(), name='categories_posts'),
   path('category/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
   path('about/', about, name='about'),
   path('contact/', contact, name='contact'),
   path('sign/', include('sign.urls')),
]