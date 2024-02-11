# Generated by Django 4.2.6 on 2023-11-06 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_wishlistmodel_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistmodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.productmodel', unique=True),
        ),
        migrations.AlterField(
            model_name='wishlistmodel',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.variantmodel', unique=True),
        ),
    ]
