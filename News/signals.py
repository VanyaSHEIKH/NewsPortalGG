from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import *
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from .tasks import send_notification

# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         category = instance.categories.all()
#         subscribers_users = []
#
#         for cat in category:
#             subscribers = cat.subscribers.all()
#             subscribers_users += [s for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_users)
#
#
# def send_notifications(preview, pk, title, subscribers):
#     for subscriber in subscribers:
#         html_content = render_to_string(
#             'post_created_email.html',
#             {
#                 'username': subscriber.username,
#                 'text': preview,
#                 'link': f'{settings.SITE_URL}/news/{pk}',
#             }
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=title,
#             body='',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[subscriber.email],
#
#         )
#
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()


# @receiver(post_save, sender=Post)
# def notify_subscribers(sender, instance, created, **kwargs):
#     if created:
#         # Получаем категории, связанные с постом
#         categories = instance.categories.all()  # используем related_name 'categories'
#         for category in categories:
#             subscribers = category.subscriber.all()  # получаем подписчиков категории
#             if not subscribers:
#                 continue
#             for subscriber in subscribers:
#                 try:
#                     send_mail(
#                         subject='Новая публикация в вашей категории',
#                         message=f'Ваша категория "{category.category}" имеет новую публикацию: {instance.title}',
#                         from_email=settings.DEFAULT_FROM_EMAIL,
#                         recipient_list=[subscriber.email],
#                     )
#                 except:
#                     print("Ошибка")


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.category.all()  # Получаем все категории поста
        category_names = [cat.category for cat in categories]  # Извлекаем имена категорий

        # Получаем всех подписчиков на эти категории
        subscribers = User.objects.filter(categories__in=categories).distinct()

        for subscriber in subscribers:
            post_url = instance.get_absolute_url()  # Получаем URL поста
            send_notification.delay(subscriber.email, subscriber.username, category_names, instance.title, post_url)