# Generated by Django 2.2.14 on 2020-07-08 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('manga', '0021_auto_20200705_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag'),
        ),
    ]