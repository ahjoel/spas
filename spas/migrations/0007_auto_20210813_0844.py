# Generated by Django 3.2.6 on 2021-08-13 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spas', '0006_alter_myuser_pseudo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_c', models.CharField(max_length=50, unique=True)),
                ('date_c', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Consommable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employe_service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_d', models.DateField()),
                ('date_f', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_e', models.CharField(max_length=50, unique=True)),
                ('date_e', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('domaine', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fourniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_type', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='employe',
            old_name='unite_organisation',
            new_name='u_orga',
        ),
        migrations.AlterField(
            model_name='myuser',
            name='pseudo',
            field=models.CharField(max_length=20, unique=True, verbose_name='Pseudo'),
        ),
        migrations.CreateModel(
            name='Sortie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_s', models.DateField()),
                ('obs_s', models.CharField(max_length=20)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.employe')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.employe_service')),
            ],
        ),
        migrations.CreateModel(
            name='Modele_mat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.type')),
            ],
        ),
        migrations.CreateModel(
            name='Materiel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_mat', models.CharField(max_length=50, unique=True)),
                ('nom', models.CharField(max_length=70, unique=True)),
                ('descrip', models.CharField(max_length=100)),
                ('mod_mat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.modele_mat')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_m', models.CharField(max_length=50)),
                ('dat_m', models.DateField()),
                ('obs_m', models.CharField(max_length=100)),
                ('mt_m', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_d', models.DateField()),
                ('date_f', models.DateField()),
                ('type_m', models.CharField(max_length=20)),
                ('etat_m', models.CharField(max_length=20)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.fournisseur')),
                ('materiel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.materiel')),
            ],
        ),
        migrations.CreateModel(
            name='Ligne_sortie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte_s', models.IntegerField()),
                ('obs_ls', models.CharField(max_length=50)),
                ('consommable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spas.consommable')),
                ('fourniture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spas.fourniture')),
                ('sortie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.sortie')),
            ],
        ),
        migrations.CreateModel(
            name='Ligne_entree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte_e', models.IntegerField()),
                ('prix_e', models.DecimalField(decimal_places=2, max_digits=10)),
                ('consommable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spas.consommable')),
                ('entree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.entree')),
                ('fourniture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spas.fourniture')),
                ('materiel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='spas.materiel')),
            ],
        ),
        migrations.CreateModel(
            name='Ligne_commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte_c', models.IntegerField()),
                ('obs_c', models.CharField(max_length=50)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.commande')),
                ('fourniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.fourniture')),
            ],
        ),
        migrations.AddField(
            model_name='fourniture',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.type'),
        ),
        migrations.AddField(
            model_name='entree',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.employe'),
        ),
        migrations.AddField(
            model_name='entree',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.fournisseur'),
        ),
        migrations.AddField(
            model_name='employe_service',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.employe'),
        ),
        migrations.AddField(
            model_name='employe_service',
            name='u_orga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.unite_organisation'),
        ),
        migrations.AddField(
            model_name='consommable',
            name='materiel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.materiel'),
        ),
        migrations.CreateModel(
            name='Affectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_d', models.DateField()),
                ('obs_d', models.CharField(max_length=100)),
                ('date_f', models.DateField(blank=True, null=True)),
                ('obs_f', models.CharField(max_length=100)),
                ('e_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spas.employe_service')),
            ],
        ),
    ]
