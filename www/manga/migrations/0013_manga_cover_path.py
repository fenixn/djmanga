# Generated by Django 2.2.13 on 2020-07-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0012_manga_url_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='cover_path',
            field=models.CharField(default='', max_length=2400),
            preserve_default=False,
        ),
    ]
