# Generated by Django 3.0.8 on 2020-07-16 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_tag_tag_tree'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_tree', models.BinaryField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tag_tree',
        ),
    ]
