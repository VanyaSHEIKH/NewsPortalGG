# Generated by Django 5.1.3 on 2024-11-13 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0003_category_category_en_us_category_category_ru_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_en_us',
        ),
        migrations.RemoveField(
            model_name='category',
            name='category_ru',
        ),
        migrations.RemoveField(
            model_name='post',
            name='text_en_us',
        ),
        migrations.RemoveField(
            model_name='post',
            name='text_ru',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title_en_us',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title_ru',
        ),
    ]
