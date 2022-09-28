from django import forms
import datetime
from django.forms import ModelChoiceField
from spas.models import Affectation, Materiel, Consommable,Employe,Employe_service,Fournisseur,Type,Fourniture,\
    Ligne_commande,Commande,Ligne_entree,Entree,MyUser,Mouvement,Maintenance,Seuil,Modele_mat,Type,\
    Unite_organisation,Ligne_sortie,Sortie

class MenuModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s %s" % (obj.u_orga,obj.employe,obj.employe.prenom)

class MenuModelChoiceField1(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class AffectationForm(forms.ModelForm):
    #materiel = MenuModelChoiceField1(queryset=Materiel.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class':'form-select'}))
    e_service = MenuModelChoiceField(queryset=Employe_service.objects.filter(etat='ACTIVE').order_by('id'),widget=forms.Select(attrs={'class': 'form-select'}))
    date_d = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    date_f = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    obs_d = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_f = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Affectation
        fields = ['materiel','e_service','date_d','date_f','obs_d','obs_f']

##########
class CommandeForm(forms.ModelForm):
    ref_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_c = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Commande
        fields = ['ref_c','date_c']

########

class MenuModelChoiceFieldc(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class ConsommableForm(forms.ModelForm):
    materiel = MenuModelChoiceFieldc(queryset=Materiel.objects.filter(etat='ACTIVE').order_by('-id'), widget=forms.Select(attrs={'class':'form-select'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Consommable
        fields = ['nom','materiel']

######

class EmployeForm(forms.ModelForm):
    u_orga = forms.ModelChoiceField(queryset=Unite_organisation.objects.filter(etat='ACTIVE').order_by('-id'), widget=forms.Select(attrs={'class':'form-select'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employe
        fields = ['nom','prenom','u_orga']

######

class MenuModelChoiceFieldemp(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.nom,obj.prenom)

class Employe_UniteForm(forms.ModelForm):
    employe = MenuModelChoiceFieldemp(queryset=Employe.objects.filter(etat='ACTIVE').order_by('-id'), widget=forms.Select(attrs={'class':'form-select'}))
    u_orga = forms.ModelChoiceField(queryset=Unite_organisation.objects.filter(etat='ACTIVE').order_by('-id'), widget=forms.Select(attrs={'class': 'form-select'}))
    date_d = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date','class':'form-control'}))
    date_f = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Employe_service
        fields = ['u_orga','employe','date_d','date_f']

########
class MenuModelChoiceFieldmligne(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class fLigne_comForm(forms.ModelForm):
    ref_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_c = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    fourniture = forms.ModelChoiceField(required=False, queryset=Fourniture.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_c = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_c = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_c = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_commande
        fields = ['ref_c','date_c','fourniture','qte_c','prix_c','obs_c']

class mLigne_comForm(forms.ModelForm):
    ref_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_c = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    materiel = MenuModelChoiceFieldmligne(required=False, queryset=Materiel.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_c = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_c = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_c = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_commande
        fields = ['ref_c','date_c','materiel','qte_c','prix_c','obs_c']

class cLigne_comForm(forms.ModelForm):
    ref_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_c = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    consommable = forms.ModelChoiceField(required=False, queryset=Consommable.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_c = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_c = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_c = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_commande
        fields = ['ref_c','date_c','consommable','qte_c','prix_c','obs_c']

##########
class MenuModelChoiceFieldmlentre(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class fLentreForm(forms.ModelForm):
    ref_e = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_e = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select','style': 'width:350px;height:40px;font-size:15px'}))
    fourniture = forms.ModelChoiceField(required=False, queryset=Ligne_commande.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_e = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_e = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_entree
        fields = ['ref_e','date_e','fournisseur','fourniture','qte_e','prix_e']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fourniture'].queryset = Ligne_commande.objects.none()


class mLentreForm(forms.ModelForm):
    ref_e = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_e = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select'}))
    materiel = forms.ModelChoiceField(required=False, queryset=Ligne_commande.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_e = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_e = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_entree
        fields = ['ref_e','date_e','fournisseur','materiel','qte_e','prix_e']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materiel'].queryset = Ligne_commande.objects.none()

class cLentreForm(forms.ModelForm):
    ref_e = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_e = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select'}))
    consommable = forms.ModelChoiceField(required=False, queryset=Consommable.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_e = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_e = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_entree
        fields = ['ref_e','date_e','fournisseur','consommable','qte_e','prix_e']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['consommable'].queryset = Consommable.objects.none()

###############
class MenuModelChoiceFieldemploye(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.nom,obj.prenom)

class MenuModelChoiceFieldservice(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.u_orga)

class fLigne_sorForm(forms.ModelForm):
    ref_s = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_s = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    employe = MenuModelChoiceFieldemploye(queryset=Employe.objects.filter(etat='ACTIVE').order_by('id'),widget=forms.Select(attrs={'class': 'form-select','id':'emp', 'name':'emp','style': 'width:250px;height:40px;font-size:15px'}))
    service = MenuModelChoiceFieldservice(queryset=Employe_service.objects.filter(etat='ACTIVE').order_by('id'),widget=forms.Select(attrs={'class': 'form-select','id':'service', 'name':'service','style': 'width:250px;height:38px;font-size:15px'}))
    fourniture = forms.ModelChoiceField(required=False, queryset=Fourniture.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_s = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    obs_ls = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_sortie
        fields = ['ref_s','date_s','employe','fourniture','qte_s','obs_ls']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Employe_service.objects.none()

##############
class FournisseurForm(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    domaine = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Fournisseur
        fields = ['nom','domaine','contact','adresse']

##########
class FournitureForm(forms.ModelForm):
    mesure = forms.ChoiceField(choices=[('BOITE', "BOITE"),('CARTON', "CARTON"),('EMBALLAGE', "EMBALLAGE"),('METRE', "METRE"),('UNITE', "UNITE")],
                               widget=forms.Select(attrs={'class':'form-select'}))
    type = forms.ModelChoiceField(queryset=Type.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class':'form-select'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    qte_seuil = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    base = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Fourniture
        fields = ['nom','qte_seuil','type','base','mesure']

##########
class MenuModelChoiceFieldlignemateriel(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class Ligne_commandeForm(forms.ModelForm):
    commande = forms.ModelChoiceField(queryset=Commande.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select'}))
    fourniture = forms.ModelChoiceField(queryset=Fourniture.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select'}))
    qte_c = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_c = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_commande
        fields = ['commande','fourniture','qte_c','prix_c','obs_c']

class Ligne_materiel_commandeForm(forms.ModelForm):
    commande = forms.ModelChoiceField(queryset=Commande.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select'}))
    materiel = MenuModelChoiceFieldlignemateriel(queryset=Materiel.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select'}))
    qte_c = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_c = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_commande
        fields = ['commande','materiel','qte_c','prix_c','obs_c']

class Ligne_consommable_commandeForm(forms.ModelForm):
    commande = forms.ModelChoiceField(queryset=Commande.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select'}))
    consommable = forms.ModelChoiceField(queryset=Consommable.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select'}))
    qte_c = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    prix_c = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_commande
        fields = ['commande','consommable','qte_c','prix_c','obs_c']

###########
class MenuModelChoiceFieldentree(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s du %s" % (obj.ref_e,obj.date_e)

class MenuModelChoiceFieldmateriel(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class Ligne_entreeForm(forms.ModelForm):
    entree = MenuModelChoiceFieldentree(queryset=Entree.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select','style': 'visibility:hidden'}))
    commande = forms.ModelChoiceField(required=False,
                                     queryset=Ligne_commande.objects.filter(etat='ACTIVE').order_by('id'),
                                     widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    fourniture = forms.ModelChoiceField(queryset=Fourniture.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select','style': 'visibility:hidden'}))
    qte_e = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    prix_e = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_entree
        fields = ['entree','commande','fourniture','qte_e','prix_e']

class Ligne_entreemForm(forms.ModelForm):
    entree = MenuModelChoiceFieldentree(queryset=Entree.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select', 'style': 'visibility:hidden'}))
    commande = forms.ModelChoiceField(required=False,
                                     queryset=Ligne_commande.objects.filter(etat='ACTIVE').order_by('id'),
                                     widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    materiel = MenuModelChoiceFieldmateriel(queryset=Materiel.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    qte_e = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    prix_e = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_entree
        fields = ['entree','commande','materiel','qte_e','prix_e']

class Ligne_entreecForm(forms.ModelForm):
    entree = MenuModelChoiceFieldentree(queryset=Entree.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select', 'style': 'visibility:hidden'}))
    commande = forms.ModelChoiceField(required=False,
                                     queryset=Ligne_commande.objects.filter(etat='ACTIVE').order_by('id'),
                                     widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    consommable = forms.ModelChoiceField(queryset=Consommable.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    qte_e = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    prix_e = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_entree
        fields = ['entree','commande','consommable','qte_e','prix_e']

##############
class MenuModelChoiceFieldsortie(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s de %s - %s" % (obj.ref_s,obj.employe,obj.employe.prenom)

class Ligne_sortieForm(forms.ModelForm):
    sortie = MenuModelChoiceFieldsortie(queryset=Sortie.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select', 'style': 'visibility:hidden'}))
    lentree = forms.ModelChoiceField(queryset=Ligne_entree.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select','style': 'visibility:hidden'}))
    fourniture = forms.ModelChoiceField(queryset=Fourniture.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    qte_s = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_ls = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_sortie
        fields = ['sortie','lentree','fourniture','qte_s','obs_ls']

class Ligne_sortiecForm(forms.ModelForm):
    sortie = MenuModelChoiceFieldsortie(queryset=Sortie.objects.order_by('-id'), widget=forms.Select(attrs={'class':'form-select', 'style': 'visibility:hidden'}))
    lentree = forms.ModelChoiceField(queryset=Ligne_entree.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select','style': 'visibility:hidden'}))
    consommable = forms.ModelChoiceField(queryset=Consommable.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'style': 'visibility:hidden'}))
    qte_s = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    obs_ls = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ligne_sortie
        fields = ['sortie','lentree','consommable','qte_s','obs_ls']

######
CHOIX_MAINTENANCE = [
    ('PREVENTIVE', 'PREVENTIVE'),
    ('CORRECTIVE', 'CORRECTIVE'),
]
class MenuModelChoiceFieldmaintenance(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.ref_mat,obj.nom)

class MaintenanceForm(forms.ModelForm):
    materiel = MenuModelChoiceFieldmaintenance(queryset=Materiel.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class':'form-select'}))
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.filter(etat='ACTIVE').order_by('id'),widget=forms.Select(attrs={'class': 'form-select'}))
    obj_m = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    dat_m = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    obs_m = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mt_m = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_d = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    date_f = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    type_m = forms.ChoiceField(choices =CHOIX_MAINTENANCE, initial='PREVENTIVE', widget=forms.Select(attrs={'class':'form-select'}), required=True)
    etat_m = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Maintenance
        fields = ['materiel','fournisseur','obj_m','dat_m','obs_m','mt_m','date_d','date_f','type_m','etat_m']

###########
class MaterielForm(forms.ModelForm):
    mod_mat = forms.ModelChoiceField(queryset=Modele_mat.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class':'form-select'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    ref_mat = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    descrip = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Materiel
        fields = ['nom','ref_mat','descrip','mod_mat']

##########
class MenuModelChoiceFieldemploye(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.nom,obj.prenom)

class MenuModelChoiceFieldservice(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.u_orga)

class CLigne_sorForm(forms.ModelForm):
    ref_s = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    date_s = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    employe = MenuModelChoiceFieldemploye(queryset=Employe.objects.filter(etat='ACTIVE').order_by('id'),widget=forms.Select(attrs={'class': 'form-select','id':'emp', 'name':'emp','style': 'width:250px;height:40px;font-size:15px'}))
    service = MenuModelChoiceFieldservice(queryset=Employe_service.objects.filter(etat='ACTIVE').order_by('id'),widget=forms.Select(attrs={'class': 'form-select','id':'service', 'name':'service','style': 'width:250px;height:38px;font-size:15px'}))
    consommable = forms.ModelChoiceField(required=False, queryset=Consommable.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class': 'form-select', 'id':'fourAdder', 'name':'fourAdder'}))
    qte_s = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    obs_ls = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ligne_sortie
        fields = ['ref_s','date_s','employe','consommable','qte_s','obs_ls']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['consommable'].queryset = Consommable.objects.none()
        self.fields['service'].queryset = Employe_service.objects.none()

##########
class Modele_matForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Type.objects.filter(etat='ACTIVE').order_by('id'), widget=forms.Select(attrs={'class':'form-select'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Modele_mat
        fields = ['nom','type']

########
class SeuilForm(forms.ModelForm):
    fourniture = ModelChoiceField(queryset=Fourniture.objects.order_by('id'),widget=forms.Select(attrs={'class': 'form-select'}))
    qte_s = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_d = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    date_f = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Seuil
        fields = ['fourniture','qte_s','date_d','date_f']

############
class TypeForm(forms.ModelForm):
    nom_type = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Type
        fields = ['nom_type']

########
class U_orgaForm(forms.ModelForm):
    nom_uo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Unite_organisation
        fields = ['nom_uo']