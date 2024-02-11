# Generated by Django 4.2.6 on 2023-12-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_productmodel_is_featured_alter_cartmodel_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitemmodel',
            name='variant',
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='color',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='product_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='size',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='subcategory',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='thickness',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_apartment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_governorates_amount',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_governorates_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_house_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_phone_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_post_code_zip',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='billing_town',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='deliverd_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='order_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('ready for dispatch', 'Ready for Dispatch'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='processing', max_length=20),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='payment_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_apartment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_company_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_house_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_post_code_zip',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='shipping_town',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]