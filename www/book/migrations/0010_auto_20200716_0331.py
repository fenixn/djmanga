# Generated by Django 3.0.8 on 2020-07-16 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_book_force_scan'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='tag_tree',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='tag_tree',
            field=models.TextField(blank=True),
        ),
    ]