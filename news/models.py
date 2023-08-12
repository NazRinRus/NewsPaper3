from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        sum_rating = 0
        sum_rating_post = 0
        sum_rating_comment_author = 0
        sum_rating_comment_post = 0
        posts = Post.objects.filter(author=self.pk)
        for i in posts:
            sum_rating_post += i.rating_post
            comment_post = Comment.objects.filter(post_com=i.pk)
            for j in comment_post:
                sum_rating_comment_post += j.rating_com
        comments_author = Comment.objects.filter(user_com=self.pk)
        for i in comments_author:
            sum_rating_comment_author += i.rating_com
        sum_rating = sum_rating_post * 3 + sum_rating_comment_author + sum_rating_comment_post
        self.rating=sum_rating
        self.save()



class Category(models.Model):
    name_cat = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name_cat.title()


class Post(models.Model):
    article_post = 'AR'
    news_post = 'NE'

    POSITIONS = [
        (article_post, 'Статья'),
        (news_post, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=article_post)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        str1 = self.text_post
        if len(str1) > 124:
            return str1[124]+'...'
        else:
            return str1

    def email_preview(self):
        str1 = self.text_post
        if len(str1) > 50:
            return str1[50]
        else:
            return str1

    def __str__(self):
        return f'{self.header.title()}: {self.author}'

    def get_absolute_url(self):
        path1 = 'news_id' if self.position == 'NE' else 'articles_id'
        return reverse(path1, args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post_com = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_com = models.ForeignKey(User, on_delete=models.CASCADE)
    text_com = models.TextField()
    datetime_com = models.DateTimeField(auto_now_add=True)
    rating_com = models.IntegerField(default=0)

    def like(self):
        self.rating_com += 1
        self.save()

    def dislike(self):
        self.rating_com -= 1
        self.save()