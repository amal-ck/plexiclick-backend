# Generated by Django 4.2.6 on 2023-11-06 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_wishlistmodel_modified_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistmodel',
            name='variant',
        ),
    ]
