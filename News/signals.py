from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tasks import send_notification
#
#
# @receiver(m2m_changed, sender=Post.category.through)
# def notify_subscribers(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         categories = instance.category.all()
#
#         subscribers = User.objects.filter(subscribed_posts__in=categories).distinct()
#
#         for subscriber in subscribers:
#             post_url = instance.get_absolute_url()
#             message = (
#                 f'Здравствуйте, {subscriber.username}!\n\n'
#                 f'В категории "{", ".join([cat.name_category for cat in categories])}" добавлена новая новость: {instance.title}.\n\n'
#                 f'Вы можете прочитать статью по следующей ссылке: {settings.SITE_URL}{post_url}'
#             )
#             try:
#                 send_mail(
#                     subject='Новая новость в вашей категории',
#                     message=message,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[subscriber.email],
#                 )
#                 print(f'Уведомление отправлено {subscriber.email}')
#             except Exception as e:
#                 print(f'Ошибка при отправке уведомления {subscriber.email}: {e}')


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'news.add_post' :
        categories = instance.category.all()
        category_names = [cat.category for cat in categories]

        subscribers = User.objects.filter(category__in=categories).distinct()

        for subscriber in subscribers:
            post_url = instance.get_absolute_url()
            send_notification.delay(subscriber.email, subscriber.username, category_names, instance.title, post_url)