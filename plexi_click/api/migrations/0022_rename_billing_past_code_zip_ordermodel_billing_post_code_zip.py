# Generated by Django 4.2.6 on 2023-11-12 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_ordermodel_governorates_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermodel',
            old_name='billing_past_code_zip',
            new_name='billing_post_code_zip',
        ),
    ]