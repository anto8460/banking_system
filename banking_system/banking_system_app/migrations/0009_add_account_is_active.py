# Generated by Django 4.0.3 on 2022-05-12 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_system_app', '0008_remove_account_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True)
        ),
    ]