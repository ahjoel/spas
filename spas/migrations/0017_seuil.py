# Generated by Django 3.2.6 on 2021-09-28 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spas', '0016_auto_20210916_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seuil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte_s', models.IntegerField()),
                ('date_d', models.DateField()),
                ('date_f', models.DateField(blank=True, null=True)),
                ('fourniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.fourniture')),
            ],
        ),
    ]
