# Generated by Django 3.2.1 on 2021-05-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('text', models.TextField(null=True)),
                ('calories', models.FloatField(null=True)),
                ('image', models.TextField(null=True)),
            ],
        ),
    ]
