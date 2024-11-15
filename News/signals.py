from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import *
from .tasks import send_notification


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.category.all()
        category_names = [cat.category for cat in categories]
        subscribers = User.objects.filter(categories__in=categories).distinct()

        for subscriber in subscribers:
            post_url = instance.get_absolute_url()  # Получаем URL поста
            send_notification.delay(subscriber.email, subscriber.username, category_names, instance.title, post_url)
