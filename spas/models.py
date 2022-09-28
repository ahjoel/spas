from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class Type(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    nom_type = models.CharField(max_length=50, unique=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_type

class Unite_organisation(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    nom_uo = models.CharField(max_length=50, unique=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nom_uo) if self.nom_uo else ''

class Employe(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    nom = models.CharField(max_length=35)
    prenom = models.CharField(max_length=25)
    u_orga = models.ForeignKey(Unite_organisation, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

# Begin - customization of users
class MyUserManager(BaseUserManager):
    def create_user(self, email, nom, prenom, pseudo, employe, password=None):
        if not email:
            raise ValueError("Email is required")
        if not nom:
            raise ValueError("Nom is required")
        if not prenom:
            raise ValueError("Prenom is required")
        if not pseudo:
            raise ValueError("Pseudo is required")

        user = self.model(
            email = self.normalize_email(email),
            nom = nom,
            prenom = prenom,
            pseudo = pseudo,
            employe = employe
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, pseudo, employe, password=None):
        user = self.create_user(
            email=email,
            nom=nom,
            prenom=prenom,
            pseudo=pseudo,
            employe=employe,
            password=password
        )
        user.is_admin =True
        user.is_staff =True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)
    email=models.EmailField(verbose_name="Email address", max_length=60, unique=True)
    nom = models.CharField(verbose_name="Nom utilisateur", max_length=35)
    prenom = models.CharField(verbose_name="Prenom utilisateur", max_length=20)
    pseudo = models.CharField(verbose_name="Pseudo", max_length=20, unique=True)
    date_joined=models.DateTimeField(auto_now_add=True, verbose_name="Date joined")
    last_login=models.DateTimeField(verbose_name="Last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD="pseudo"

    REQUIRED_FIELDS = ['nom','prenom','email']

    objects = MyUserManager()
    def __str__(self):
        return self.nom

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
# End - customization of users

# Begin - signal between employe and users
@receiver(post_save, sender=Employe)
def build_myuser(sender, instance, created, **kwargs):
        if created:
            unom = instance.nom
            uprenom = instance.prenom
            traitement = uprenom.split().pop(0)
            pseudo_user = unom[0]+traitement
            email_user = traitement+'@baco.tg'
            MyUser.objects.create(nom=instance.nom, prenom=instance.prenom, pseudo=pseudo_user, email=email_user, employe=instance)
            instance.myuser.set_password(pseudo_user)

@receiver(post_save, sender=Employe)
def save_myuser(sender, instance, **kwargs):
        instance.myuser.save()

# End - signal between employe and users

class Employe_service(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    u_orga = models.ForeignKey(Unite_organisation, on_delete=models.CASCADE)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_d = models.DateField()
    date_f = models.DateField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.u_orga

class Modele_mat(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50, unique=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Materiel(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    mod_mat = models.ForeignKey(Modele_mat, on_delete=models.CASCADE)
    ref_mat = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=70, unique=True)
    descrip = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ref_mat

class Affectation(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    e_service = models.ForeignKey(Employe_service, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    date_d = models.DateField()
    obs_d = models.CharField(max_length=100)
    date_f = models.DateField(null=True, blank=True)
    obs_f = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.e_service

class Consommable(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50, unique=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    nom = models.CharField(max_length=50, unique=True)
    domaine = models.CharField(max_length=50)
    contact = models.CharField(max_length=30)
    adresse = models.CharField(max_length=50)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Maintenance(models.Model):
    PREVENTIVE = 'PREVENTIVE'
    CORRECTIVE = 'CORRECTIVE'
    CHOIX_MAINTENANCE = [
        (PREVENTIVE, 'PREVENTIVE'),
        (CORRECTIVE, 'CORRECTIVE'),
    ]
    type_m = models.CharField(
        max_length=11,
        choices=CHOIX_MAINTENANCE,
        default=PREVENTIVE,
    )
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    obj_m = models.CharField(max_length=50)
    dat_m = models.DateField()
    obs_m = models.CharField(max_length=100, null=True)
    mt_m = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    date_d = models.DateField(null=True)
    date_f = models.DateField(null=True)
    etat_m = models.CharField(max_length=20, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.materiel

class Fourniture(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    nom = models.CharField(max_length=60, unique=True)
    qte_seuil = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    base = models.IntegerField()
    mesure = models.CharField(max_length=15)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nom)


class Entree(models.Model):
    employe = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    ref_e = models.CharField(max_length=50, unique=True)
    date_e = models.DateField()
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ref_e

class Commande(models.Model):
    ref_c = models.CharField(max_length=50, unique=True)
    date_c = models.DateField()
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ref_c

class Ligne_commande(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    EN_COURS = 'EN COURS'
    LIVREE = 'LIVREE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    CHOIX_S = [
        (EN_COURS, 'EN COURS'),
        (LIVREE, 'LIVREE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    statut = models.CharField(
        max_length=15,
        choices=CHOIX_S,
        default=EN_COURS,
    )
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE, null=True)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, null=True)
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE, null=True)
    qte_c = models.IntegerField()
    prix_c = models.DecimalField(max_digits=10, decimal_places=2)
    obs_c = models.CharField(max_length=50)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.commande)

class Ligne_entree(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    EN_COURS = 'EN COURS'
    EPUISEE = 'EPUISEE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    CHOIX_STA = [
        (EN_COURS, 'EN COURS'),
        (EPUISEE, 'EPUISEE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    statut = models.CharField(
        max_length=15,
        choices=CHOIX_STA,
        default=EN_COURS,
    )
    entree = models.ForeignKey(Entree, on_delete=models.CASCADE)
    commande = models.ForeignKey(Ligne_commande, on_delete=models.CASCADE)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, null=True)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE, null=True)
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE, null=True)
    qte_e = models.IntegerField()
    prix_e = models.DecimalField(max_digits=10, decimal_places=2)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.qte_e * self.prix_e

    def __str__(self):
        return str(self.entree)

class Sortie(models.Model):
    ref_s = models.CharField(max_length=50, unique=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_s = models.DateField()
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ref_s

class Ligne_sortie(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    sortie = models.ForeignKey(Sortie, on_delete=models.CASCADE)
    lentree = models.ForeignKey(Ligne_entree, on_delete=models.CASCADE)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, null=True)
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE, null=True)
    qte_s = models.IntegerField()
    obs_ls = models.CharField(max_length=50)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sortie

class Mouvement(models.Model):
    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    CHOIX = [
        (INACTIVE, 'INACTIVE'),
        (ACTIVE, 'ACTIVE'),
    ]
    etat = models.CharField(
        max_length=15,
        choices=CHOIX,
        default=ACTIVE,
    )
    date_m = models.DateField()
    ligne_sortie = models.ForeignKey(Ligne_sortie, on_delete=models.CASCADE, null=True)
    ligne_appro = models.ForeignKey(Ligne_entree, on_delete=models.CASCADE, null=True)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, null=True)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE, null=True)
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE, null=True)
    qte = models.IntegerField()
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    APPRO = 'APPRO'
    SORTIE = 'SORTIE'
    CHOIX_MOUVEMENT = [
        (APPRO, 'APPRO'),
        (SORTIE, 'SORTIE'),
    ]
    type = models.CharField(
        max_length=8,
        choices=CHOIX_MOUVEMENT,
        default=APPRO,
    )

    def __str__(self):
        return self.ligne_sortie


class Seuil(models.Model):
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE)
    qte_s = models.IntegerField()
    date_d = models.DateField()
    date_f = models.DateField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fourniture
