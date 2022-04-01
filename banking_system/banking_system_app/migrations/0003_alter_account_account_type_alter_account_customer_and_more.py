# Generated by Django 4.0.3 on 2022-04-01 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banking_system_app', '0002_alter_account_id_alter_accounttype_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='banking_system_app.accounttype'),
        ),
        migrations.AlterField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='banking_system_app.customer'),
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.UUIDField(default=uuid.UUID('aa585958-8172-4649-9be5-a1ca35747fe8'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='accountstransaction',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='banking_system_app.transaction'),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='id',
            field=models.UUIDField(default=uuid.UUID('575325a1-a158-4411-8886-769ba3f45dca'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bankdetail',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='banking_system_app.account'),
        ),
        migrations.AlterField(
            model_name='bankdetail',
            name='id',
            field=models.UUIDField(default=uuid.UUID('74805de6-dee0-48ad-aa11-5a5510368d34'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.UUIDField(default=uuid.UUID('38c92cfc-2588-49db-9729-afd0020aa422'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.UUIDField(default=uuid.UUID('318e622f-d2ec-4c6a-b6c9-599343da0380'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loan',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='banking_system_app.customer'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='id',
            field=models.UUIDField(default=uuid.UUID('22561d30-39a7-4944-b025-bd5413fa24f6'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.UUIDField(default=uuid.UUID('887ad967-a3db-4dee-9927-774bc0ea9d4d'), editable=False, primary_key=True, serialize=False),
        ),
    ]
