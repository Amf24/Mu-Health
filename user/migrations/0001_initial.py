# Generated by Django 3.2.1 on 2021-05-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=255, null=True)),
                ('height', models.PositiveIntegerField(null=True)),
                ('goal_type', models.CharField(choices=[('lose weight', 'lose wight'), ('gain weight', 'gain weight')], max_length=255, null=True)),
                ('wight', models.FloatField(null=True)),
            ],
        ),
    ]
