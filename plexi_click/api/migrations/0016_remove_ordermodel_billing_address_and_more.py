# Generated by Django 4.2.6 on 2023-11-11 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_rename_order_status_reviewsmodel_review_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='shipping_address',
        ),
    ]