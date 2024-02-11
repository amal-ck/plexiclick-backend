# Generated by Django 4.2.6 on 2023-11-08 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_wishlistmodel_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddressmodel',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='shippingaddressmodel',
            name='email',
        ),
        migrations.RemoveField(
            model_name='shippingaddressmodel',
            name='governorates',
        ),
        migrations.RemoveField(
            model_name='shippingaddressmodel',
            name='phone_no',
        ),
        migrations.AddField(
            model_name='billingaddressmodel',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='billingaddressmodel',
            name='governorates',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.governoratesmodel'),
        ),
        migrations.AddField(
            model_name='billingaddressmodel',
            name='phone_no',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='shippingaddressmodel',
            name='company_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]