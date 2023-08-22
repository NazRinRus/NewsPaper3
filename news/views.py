from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache
import logging


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти / Зарегистрироваться", 'url_name': '/accounts/login'}
]

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    logging.error('test_debug')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.all()
        context['menu'] = menu
        context['title'] = 'Все посты'
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class CategoryList(ListView): #Просмотр всех категорий с возможностью подписки
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категории постов'
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['cat_user'] = Category.objects.filter(subscribers__username=self.request.user.username)
        return context

class CategoryListView(ListView): #Просмотр всех постов соответствующих конкретной категории
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category,id = self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты по категориям'
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

class PostListNews(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(position='NE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.filter(position = 'NE').order_by('-time_in')
        context['menu'] = menu
        context['title'] = 'Новости'
        return context

class PostListArticles(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(position='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.filter(position = 'AR').order_by('-time_in')
        context['menu'] = menu
        context['title'] = 'Статьи'
        return context



class NewsSearch(ListView): #Класс для фильтрации новостей
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(position='NE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.filter(position = 'NE').order_by('-time_in')
        context['filterset'] = self.filterset
        context['title'] = 'Поиск новостей'
        return context

class ArticlesSearch(ListView): #Класс для фильтрации новостей
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(position='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.filter(position = 'AR').order_by('-time_in')
        context['filterset'] = self.filterset
        context['title'] = 'Поиск статей'
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj

class PostDetailNews(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        return context
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj

class PostDetailArticles(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        return context
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/news/create/':
            post.position = 'NE'
        if self.request.path == '/posts/articles/create/':
            post.position = 'AR'
        post.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        context['user'] = self.request.user.username
        return context

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        return context

class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_all')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        return context

class ArticlesDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles_all')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Все посты'
        return context

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def about(request):
    return render(request, 'news/about.html', {'menu': menu, 'title': 'О сайте'})

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей категории'
    #return render(request, 'subscribe.html', {'category': category, 'message': message})
    return redirect('categories_posts')

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы отписались от рассылки новостей категории'
    #return render(request, 'subscribe.html', {'category': category, 'message': message})
    return redirect('categories_posts')