# Generated by Django 2.2.14 on 2020-07-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_book_book_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='dir_last_update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='directory last update date'),
        ),
    ]
