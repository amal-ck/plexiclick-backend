# Generated by Django 4.2.6 on 2023-11-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_ordermodel_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='governorates_amount',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='governorates_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]