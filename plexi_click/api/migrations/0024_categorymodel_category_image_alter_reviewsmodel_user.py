# Generated by Django 4.2.6 on 2023-11-17 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0023_reviewsmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='category_image',
            field=models.ImageField(null=True, upload_to='category_images'),
        ),
        migrations.AlterField(
            model_name='reviewsmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]