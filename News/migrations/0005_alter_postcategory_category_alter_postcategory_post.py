# Generated by Django 5.1.3 on 2024-11-14 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0004_remove_category_category_en_us_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='News.category'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='News.post'),
        ),
    ]
