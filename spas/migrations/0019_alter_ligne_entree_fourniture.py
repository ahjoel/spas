# Generated by Django 3.2.6 on 2021-10-04 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spas', '0018_auto_20211004_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ligne_entree',
            name='fourniture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spas.ligne_commande'),
        ),
    ]
