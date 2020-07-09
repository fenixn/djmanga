# Generated by Django 2.2.13 on 2020-07-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0019_chapter_read_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='illustrator',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='manga',
            name='author',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]