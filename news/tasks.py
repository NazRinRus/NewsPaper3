import datetime

from NewsPaper.celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
import NewsPaper.settings


@shared_task
def send_mail_subscriber(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    subscribers: list[str] = []
    title = post.title
    for category in categories:
        subscribers += category.subscribers.all()
    subscribers_emails = [s.email for s in subscribers]

    html_context = render_to_string(
        'mail/new_post_notification.html',
        {
            'post': post.email_preview(),
            'category': category,
            'link': NewsPaper.settings.SITE_URL,

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='rnazarov11@bk.ru',
        to=subscribers_emails
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task
def send_weekly_mail():
    start_date = datetime.datetime.today() - datetime.timedelta(days=6)
    this_weeks_posts = Post.objects.filter(time_in__gt=start_date)
    for cat in Category.objects.all():
        post_list = this_weeks_posts.filter(category=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            html_content = render_to_string(
                'mail/new_posts.html', {
                    'link': NewsPaper.settings.SITE_URL,
                    'posts': post_list,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Категория - {cat.name_cat}',
                body="---------",
                from_email=NewsPaper.settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
    print('рассылка произведена')