# Generated by Django 3.2.5 on 2022-04-16 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
