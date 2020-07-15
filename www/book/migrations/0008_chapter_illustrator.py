# Generated by Django 2.2.14 on 2020-07-15 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20200713_1522'),
        ('book', '0007_chapter_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='illustrator',
            field=models.ManyToManyField(related_name='chapterillustrator', to='person.Person'),
        ),
    ]
