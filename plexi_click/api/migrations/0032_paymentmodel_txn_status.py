# Generated by Django 4.2.6 on 2023-12-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_rename_txn_id_paymentmodel_txn_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='txn_status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
