# Generated by Django 5.0.3 on 2024-03-12 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='author',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
