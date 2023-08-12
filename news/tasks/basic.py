from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
import NewsPaper.settings

def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


def new_post_notification(instance):
    template = 'mail/new_post_notification.html'
    for category in instance.category.all():
        email_subject = f'Новый пост в категории: "{category}"'
        user_emails = get_subscriber(category)
        html = render_to_string(
            template_name=template,
            context={
                'category': category,
                'link': NewsPaper.settings.SITE_URL,
                'users': category.subscribers.all(),
                'post': instance,
            },
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email='rnazarov11@bk.ru',
            to=user_emails
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()