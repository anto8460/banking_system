# Generated by Django 4.0.3 on 2022-05-10 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_system_app', '0004_alter_account_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
