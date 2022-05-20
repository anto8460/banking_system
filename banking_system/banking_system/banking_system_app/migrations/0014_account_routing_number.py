# Generated by Django 4.0.3 on 2022-05-19 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking_system_app', '0013_knownbank_is_local'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='routing_number',
            field=models.ForeignKey(default='e464d49d-4742-40dc-83be-98c682dc0840', on_delete=django.db.models.deletion.DO_NOTHING, to='banking_system_app.knownbank'),
            preserve_default=False,
        ),
    ]
