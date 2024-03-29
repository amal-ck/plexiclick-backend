# Generated by Django 4.2.6 on 2023-11-01 09:21

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddressModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('house_no_street_name', models.CharField(max_length=100, null=True)),
                ('apartment', models.CharField(max_length=200, null=True)),
                ('town_or_city', models.CharField(max_length=200, null=True)),
                ('post_code_zip', models.CharField(max_length=11, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ColorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(max_length=100, null=True)),
                ('color_code', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None)),
            ],
        ),
        migrations.CreateModel(
            name='GovernoratesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('governorates', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('order_status', models.CharField(choices=[('processing', 'Processing'), ('ready_for_dispatch', 'Ready for Dispatch'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='processing', max_length=20)),
                ('deliverd_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('billing_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.billingaddressmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Productmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_desc', models.TextField(null=True)),
                ('product_image', models.ImageField(null=True, upload_to='product_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.categorymodel')),
            ],
        ),
        migrations.CreateModel(
            name='SizeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThicknessModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thickness', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VariantModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_image', models.ImageField(null=True, upload_to='variant_images')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('stock', models.IntegerField(null=True)),
                ('reorder_level', models.IntegerField(null=True)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.colormodel')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.productmodel')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.sizemodel')),
                ('thickness', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.thicknessmodel')),
            ],
        ),
        migrations.CreateModel(
            name='WishlistModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.productmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.variantmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddressModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('house_no_street_name', models.CharField(max_length=100, null=True)),
                ('apartment', models.CharField(max_length=200, null=True)),
                ('town_or_city', models.CharField(max_length=200, null=True)),
                ('post_code_zip', models.CharField(max_length=11, null=True)),
                ('phone_no', models.IntegerField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('governorates', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.governoratesmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('rating', models.IntegerField(null=True)),
                ('review', models.TextField(max_length=350, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.productmodel')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_id', models.CharField(max_length=100, null=True)),
                ('bank_txn_id', models.CharField(max_length=100, null=True)),
                ('txn_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('txn_type', models.CharField(max_length=100, null=True)),
                ('gateway_name', models.CharField(max_length=100, null=True)),
                ('bank_name', models.CharField(max_length=100, null=True)),
                ('mid', models.IntegerField(null=True)),
                ('payment_mode', models.CharField(max_length=100, null=True)),
                ('txn_date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.ordermodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.shippingaddressmodel'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ordermodel')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.productmodel')),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.variantmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.productmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.variantmodel')),
            ],
        ),
    ]
