# Generated by Django 3.2.1 on 2021-05-06 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210506_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='foodlist',
        ),
    ]
