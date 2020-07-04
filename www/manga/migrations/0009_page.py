# Generated by Django 2.2.13 on 2020-07-04 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0008_chapter_folder_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField(default=1)),
                ('page_file', models.CharField(max_length=200)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.Chapter')),
            ],
        ),
    ]