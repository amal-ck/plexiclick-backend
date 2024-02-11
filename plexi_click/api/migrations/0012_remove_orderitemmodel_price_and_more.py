# Generated by Django 4.2.6 on 2023-11-10 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_cartmodel_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitemmodel',
            name='price',
        ),
        migrations.RemoveField(
            model_name='orderitemmodel',
            name='product',
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='total_amount',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='txn_amount',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='variantmodel',
            name='product_price',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='variantmodel',
            name='sale_price',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
    ]