# Generated by Django 4.0.3 on 2022-05-10 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_system_app', '0005_alter_userinformation_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
    ]
