# Generated by Django 3.2.6 on 2021-08-25 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spas', '0011_auto_20210824_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='ref_c',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='entree',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
