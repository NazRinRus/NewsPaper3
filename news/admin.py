from django.contrib import admin
from .models import Author, Comment, Category, Post, PostCategory

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('header', 'author')

# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
