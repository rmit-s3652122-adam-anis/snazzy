# Generated by Django 2.2.4 on 2019-09-22 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20190922_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]