# Generated by Django 2.2.13 on 2020-07-03 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=200)),
                ('folder_name', models.CharField(max_length=1000)),
                ('folder_path', models.CharField(max_length=1200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('add_date', models.DateTimeField(verbose_name='date added')),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
