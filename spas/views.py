from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from django.db.models import Sum
from django.views.generic import View
from .utils import render_to_pdf
from datetime import date
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import *
from django.conf import settings

# Connexion de l'application.
def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':
            pseudo = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=pseudo, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                 messages.error(request, "Svp, le pseudo et le mot de passe sont incorrectes.")

    return render(request, 'registration/login.html')


# Création de la page d'acceuil de l'application.
def indext(request):
    return render(request, 'base.html')

# Page d'acceuil
@login_required
def index(request):
    #return HttpResponse('bonjour à tous')
    return render(request, 'accueil.html')


### Gestion du stock

#Liste - type.
@login_required
def list_type(request):
    types = Type.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(types, 10)
    page = request.GET.get('page')
    try:
        types = paginator.page(page)
    except PageNotAnInteger:
        types = paginator.page(1)
    except EmptyPage:
        types = paginator.page(paginator.num_pages)

    context = {'types': types,'paginator':paginator}
    return render(request, 'stock/fournitures/type/type.html', context)


#Création - type
def create_type(request):
    form = TypeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_type')

    return render(request, 'stock/fournitures/type/type_form.html', {'form': form})


#MAJ - type
def update_type(request, id):
    type = get_object_or_404(Type,id=id)
    form = TypeForm(request.POST or None, instance=type)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_type')

    return render(request, 'stock/fournitures/type/type_form.html', {'form': form})


#Suppression - type
def delete_type(request, id):
    type = get_object_or_404(Type,id=id)

    if request.method == 'POST':
        type.etat = 'INACTIVE'
        type.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_type')

    return render(request, 'stock/fournitures/type/type_sup_confirm.html', {'type': type})


#Liste - fourniture
@login_required
def list_fourniture(request):
    fours = Fourniture.objects.filter(etat='ACTIVE').order_by('id') # par ordre décroissant
    paginator = Paginator(fours, 10)
    page = request.GET.get('page')
    try:
        fours = paginator.page(page)
    except PageNotAnInteger:
        fours = paginator.page(1)
    except EmptyPage:
        fours = paginator.page(paginator.num_pages)

    context = {'fours': fours,'paginator':paginator}
    return render(request, 'stock/fournitures/fourniture/fourniture.html', context)


#Création - fourniture
def create_fourniture(request):
    form = FournitureForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_fourniture')

    return render(request, 'stock/fournitures/fourniture/fourniture_form.html', {'form': form})


#MAJ - fourniture
def update_fourniture(request, id):
    four = get_object_or_404(Fourniture,id=id)
    form = FournitureForm(request.POST or None, instance=four)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_fourniture')

    return render(request, 'stock/fournitures/fourniture/fourniture_form.html', {'form': form})


#Suppression - fourniture
def delete_fourniture(request, id):
    four = get_object_or_404(Fourniture,id=id)

    if request.method == 'POST':
        four.etat = 'INACTIVE'
        four.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_fourniture')

    return render(request, 'stock/fournitures/fourniture/fourniture_sup_confirm.html', {'four': four})


# recherhe des fournitures
def search_fourniture(request):

    if request.method == "GET" and 'req_f' in request.GET:
        req_f = request.GET.get('req_f')
        if (req_f != None and req_f != ''):
            fours = Fourniture.objects.filter(nom__icontains=req_f, etat='ACTIVE')
            context = {'req_f': req_f, 'fours': fours}
            return render(request, 'stock/fournitures/fourniture/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/fournitures/fourniture/search.html')

# Commande pour fourniture (fourniture_commande).

#Liste - fourniture commandé
@login_required
def list_lcommande(request):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_commande.id,spas_commande.date_c,spas_commande.ref_c,count(spas_ligne_commande.fourniture_id) as nbfour, 
                sum(spas_ligne_commande.qte_c) as qte_total,sum(spas_ligne_commande.prix_c) as prix_total
                from spas_ligne_commande,spas_commande,spas_fourniture
                where spas_ligne_commande.fourniture_id=spas_fourniture.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                group by spas_commande.id,spas_commande.date_c,spas_commande.ref_c
                order by spas_commande.ref_c desc
            """

    lcoms = Commande.objects.raw(query, [active, en_cours])
    #lcoms = Ligne_commande.objects.order_by('-id')  par ordre décroissant
    paginator = Paginator(lcoms, 10)
    page = request.GET.get('page')
    try:
        lcoms = paginator.page(page)
    except PageNotAnInteger:
        lcoms = paginator.page(1)
    except EmptyPage:
        lcoms = paginator.page(paginator.num_pages)

    context = {'lcoms': lcoms,'paginator':paginator}
    return render(request, 'stock/fournitures/lcommande/lcommande.html', context)


#Liste détaillé - fourniture commandé
def detail_lcommande(request, id):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_commande.id,spas_fourniture.nom,spas_ligne_commande.qte_c,spas_ligne_commande.prix_c,
                spas_commande.ref_c,spas_commande.date_c,spas_ligne_commande.obs_c
                from spas_ligne_commande,spas_commande,spas_fourniture
                where spas_ligne_commande.fourniture_id=spas_fourniture.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_commande.id=%s
            """

    lcoms = Ligne_commande.objects.raw(query, [active, en_cours, id])
    paginator = Paginator(lcoms, 10)
    page = request.GET.get('page')
    try:
        lcoms = paginator.page(page)
    except PageNotAnInteger:
        lcoms = paginator.page(1)
    except EmptyPage:
        lcoms = paginator.page(paginator.num_pages)

    context = {'lcoms': lcoms,'paginator':paginator}
    return render(request, 'stock/fournitures/lcommande/lcommande_detail.html', context)


# recherhe des fournitures commandées
def search_fourniture_commandee(request):

    if request.method == "GET" and 'date_fcmd' in request.GET:
        date_fcmd = request.GET.get('date_fcmd')
        if (date_fcmd != ''):
            fcmds = Ligne_commande.objects.filter(commande__date_c=date_fcmd, etat='ACTIVE')
            context = {'date_fcmd': date_fcmd, 'fcmds': fcmds}
            return render(request, 'stock/fournitures/lcommande/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/fournitures/lcommande/search.html')


#Création unique - fourniture commandé
def create_lcommande(request):
    form = Ligne_commandeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lcommande')

    return render(request, 'stock/fournitures/lcommande/lcommande_form.html', {'form': form})


#Création multiple - fourniture commandé
def create_flcom(request):
    form = fLigne_comForm(request.POST or None)
    d = date.today().strftime("%d%m%Y")
    id_max = Commande.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_com = "CMD0" + str(id_max) + str(d)
    if request.method=='POST':
        date_com = request.POST['date_c']
        ref_com = request.POST['ref_c']
        four = request.POST.getlist('fourIds[]')
        qte = request.POST.getlist('qtefour[]')
        obs = request.POST.getlist('obs_c[]')
        prix = request.POST.getlist('prices[]')
        if (four):
            com = Commande.objects.create(ref_c=ref_com, date_c=date_com)
            commande_id = com.id
            for i in range(len(four)):
                Ligne_commande.objects.create(commande=Commande.objects.get(pk=commande_id), fourniture=Fourniture.objects.get(pk=four[i]), qte_c=qte[i], prix_c=prix[i], obs_c=obs[i])

            messages.success(request, "Enregistrement(s) effectué(s)")
            return redirect('list_lcommande')
        else:
            messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne commande de fourniture.")
            return render(request, 'stock/fournitures/lcommande/flcom_form.html', {'form': form, 'ref': ref_com})

    return render(request, 'stock/fournitures/lcommande/flcom_form.html', {'form': form,'ref':ref_com})


#MAJ - fourniture commandé
def update_lcommande(request, id):
    com = get_object_or_404(Ligne_commande,id=id)
    form = Ligne_commandeForm(request.POST or None, instance=com)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_lcommande')

    return render(request, 'stock/fournitures/lcommande/lcommande_form.html', {'form': form})


#Suppression - fourniture commandé
def delete_lcommande(request, id):
    lcom = get_object_or_404(Ligne_commande,id=id)

    if request.method == 'POST':
        lcom.etat = 'INACTIVE'
        lcom.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_lcommande')

    return render(request, 'stock/fournitures/lcommande/lcommande_sup_confirm.html', {'lcom': lcom})

# Approvisionnement pour fourniture (fourniture_entree).

#Liste - fourniture approvisionné
@login_required
def list_lentree(request):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_entree.id,spas_entree.date_e,spas_entree.ref_e,count(spas_ligne_entree.fourniture_id) as nbfour,
                sum(spas_ligne_entree.qte_e) as qte_total,sum(spas_ligne_entree.prix_e) as prix_total
                from spas_ligne_entree,spas_entree,spas_fourniture
                where spas_ligne_entree.fourniture_id=spas_fourniture.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
                group by spas_entree.id,spas_entree.date_e,spas_entree.ref_e
                order by spas_entree.ref_e desc
            """

    lents = Entree.objects.raw(query, [active, en_cours])
    paginator = Paginator(lents, 10)
    page = request.GET.get('page')
    try:
        lents = paginator.page(page)
    except PageNotAnInteger:
        lents = paginator.page(1)
    except EmptyPage:
        lents = paginator.page(paginator.num_pages)

    context = {'lents': lents,'paginator':paginator}
    return render(request, 'stock/fournitures/lentree/lentree.html', context)


# recherhe des fournitures entrées
def search_fourniture_entree(request):

    if request.method == "GET" and 'date_fent' in request.GET:
        date_fent = request.GET.get('date_fent')
        if (date_fent != ''):
            fents = Ligne_entree.objects.filter(entree__date_e=date_fent, etat='ACTIVE')
            context = {'date_fent': date_fent, 'fents': fents}
            return render(request, 'stock/fournitures/lentree/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/fournitures/lentree/search.html')


#Liste détaillé - fourniture approvisionné
def detail_list_lentree(request, id):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_entree.id,spas_fourniture.nom,spas_ligne_entree.qte_e,
                spas_ligne_entree.prix_e,spas_entree.ref_e,spas_entree.date_e
                from spas_ligne_entree,spas_fourniture,spas_entree
                where spas_ligne_entree.fourniture_id=spas_fourniture.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
                and spas_ligne_entree.entree_id=%s
            """

    lents = Ligne_entree.objects.raw(query, [active, en_cours, id])
    paginator = Paginator(lents, 10)
    page = request.GET.get('page')
    try:
        lents = paginator.page(page)
    except PageNotAnInteger:
        lents = paginator.page(1)
    except EmptyPage:
        lents = paginator.page(paginator.num_pages)

    context = {'lents': lents,'paginator':paginator}
    return render(request, 'stock/fournitures/lentree/lentree_detail.html', context)


#Création unique - fourniture approvisionné
def create_lentree(request):
    form = Ligne_entreeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lentree')

    return render(request, 'stock/fournitures/lentree/lentree_form.html', {'form': form})


#Chargement de la liste déroulante des fournitures commandés sur la page des fourniture approvisionné
def load_fourniture_cmd(request):
    cmd_ref = request.GET.get('cmd_ref')
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_commande.id, spas_ligne_commande.fourniture_id,
                spas_fourniture.nom,spas_ligne_commande.qte_c,spas_ligne_commande.prix_c
                from spas_ligne_commande,spas_commande,spas_fourniture
                where spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.fourniture_id=spas_fourniture.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_commande.ref_c=%s
            """

    f_cmds = Ligne_commande.objects.raw(query, [active, en_cours,cmd_ref])
    return render(request, 'stock/fournitures/lentree/fourniture_cmd.html', {'f_cmds': f_cmds})


#Création multiple - fourniture approvisionné
def create_flent(request):
    form = fLentreForm(request.POST or None)
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select distinct spas_commande.id,spas_commande.ref_c
                from spas_ligne_commande,spas_commande
                where spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_ligne_commande.fourniture_id is not null 
                order by spas_commande.ref_c desc
            """

    commande = Commande.objects.raw(query,[active, en_cours])
    d = date.today().strftime("%d%m%Y")
    id_max = Entree.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_ent = "APPRO" + str(id_max) + str(d)
    if request.method=='POST':
        date_e = request.POST['date_e']
        ref_e = request.POST['ref_e']
        fournis = request.POST['fournisseur']
        employe = request.user.id
        four_commande = request.POST.getlist('fourIds[]') #four_commande represente la ligne commande ou il y a la fourniture cmdé
        fournit_id = request.POST.getlist('FournitId[]') #fournit_id represente l'id de la fourniture en question
        qte = request.POST.getlist('qtefour[]')
        prix = request.POST.getlist('prices[]')
        if (date_e and ref_e and fournis and employe):
            if (four_commande and fournit_id):
                ent = Entree.objects.create(ref_e=ref_e, date_e=date_e, fournisseur=Fournisseur.objects.get(pk=fournis),employe=MyUser.objects.get(pk=employe))
                entree_id = ent.id
                for i in range(len(four_commande)):
                    four_commande_entree = Ligne_entree.objects.create(entree=Entree.objects.get(pk=entree_id), commande=Ligne_commande.objects.get(pk=four_commande[i]), fourniture=Fourniture.objects.get(pk=fournit_id[i]), qte_e=qte[i], prix_e=prix[i])
                    cmd_entree_id = four_commande_entree.id
                    Mouvement.objects.create(date_m=date_e, ligne_appro=Ligne_entree.objects.get(pk=cmd_entree_id), fourniture=Fourniture.objects.get(pk=fournit_id[i]), qte=qte[i], type='APPRO')
                    Ligne_commande.objects.filter(id=four_commande[i]).update(statut='LIVREE')

                messages.success(request, "Enregistrement(s) effectué(s)")
                return redirect('list_lentree')
            else:
                messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne de fourniture.")
                return render(request, 'stock/fournitures/lentree/flentre_form.html', {'form': form, 'ref': ref_ent,'commande':commande})
        else:
            messages.warning(request, "Svp, Veuillez remplir toutes les zones de saisies.")
            return render(request, 'stock/fournitures/lentree/flentre_form.html', {'form': form, 'ref': ref_ent,'commande':commande})

    return render(request, 'stock/fournitures/lentree/flentre_form.html', {'form': form,'ref':ref_ent,'commande':commande})


#Chargement automatique de l'id de la fourniture sur la page entree(appro)
def load_fourniture(request):
    com_id = request.GET.get('ligne_commande')
    #fournit_id = Ligne_commande.objects.filter(id=com_id)
    fournit_id = get_object_or_404(Ligne_commande,id=com_id)
    fId = fournit_id.fourniture.id
    return JsonResponse(fId, safe=False)


#MAJ - fourniture approvisionné
def update_lentree(request, id):
    ent = get_object_or_404(Ligne_entree,id=id)
    mouv = get_object_or_404(Mouvement,ligne_appro_id=ent)
    form_f = Ligne_entreeForm(request.POST or None, instance=ent)

    #verification si la livraison est déja utilisé(présent dans la table sortie)
    ent_utilise = list(Ligne_sortie.objects.filter(lentree_id=id,etat='ACTIVE').aggregate(Sum('lentree')).values())[0] or 0
    
    if form_f.is_valid():
        if ent_utilise == 0:
            postf = form_f.save(commit=False)
            # Mise a jour automatique des donnees de la table mouvement
            details = get_object_or_404(Entree,ref_e=postf.entree)
            date_entree = details.date_e
            mouv.date_m = date_entree
            mouv.fourniture = postf.fourniture
            mouv.qte = postf.qte_e
            # Fin de la Mise a jour automatique des donnees de la table mouvement
            postf.save()
            mouv.save()
            messages.success(request, "Modification effectuée")
            return redirect('list_lentree')
        else:
            messages.success(request, "Modification impossible, la livraison est en utilisation ")
            return redirect('list_lentree')

    return render(request, 'stock/fournitures/lentree/lentree_form.html', {'form': form_f, 'ent':ent})


#Suppression - fourniture approvisionné
def delete_lentree(request, id):
    lent = get_object_or_404(Ligne_entree,id=id)
    mouv = get_object_or_404(Mouvement,ligne_appro_id=lent)

    #verification si la livraison est déja utilisé(présent dans la table sortie)
    lent_utilise = list(Ligne_sortie.objects.filter(lentree_id=id,etat='ACTIVE').aggregate(Sum('lentree')).values())[0] or 0

    if request.method == 'POST':
        if lent_utilise == 0:
            commande_id = lent.commande_id
            Ligne_commande.objects.filter(id=commande_id).update(statut='EN COURS')
            mouv.etat = 'INACTIVE'
            lent.etat = 'INACTIVE'
            mouv.save()
            lent.save()
            # permet d'actualiser la ligne commande ou la fourniture est en cours au cas ou il serait préalablement livrée dans
            # la table ligne commande
            #Ligne_commande.objects.filter(fourniture_id=lent.fourniture_id).update(statut='EN COURS')
            messages.success(request, "Suppression effectuée")
            return redirect('list_lentree')
        else:
            messages.success(request, "Suppression impossible, la livraison est en utilisation.")
            return redirect('list_lentree')

    return render(request, 'stock/fournitures/lentree/lentree_sup_confirm.html', {'lent': lent})

# Sortie pour fourniture (fourniture_sortie).

#Liste - fourniture sortie
@login_required
def list_lsortie(request):
    #lsors = Ligne_sortie.objects.filter(etat='ACTIVE', fourniture__isnull=False).order_by('-id') # par ordre décroissant
    active = 'ACTIVE'
    query = """
               select spas_sortie.id,spas_sortie.date_s,spas_sortie.ref_s,count(spas_ligne_sortie.fourniture_id) as nbfour,
               sum(spas_ligne_sortie.qte_s) as qte_total,concat(spas_employe.nom,' ',spas_employe.prenom) as np
               from spas_ligne_sortie,spas_sortie,spas_fourniture,spas_employe
               where spas_ligne_sortie.fourniture_id=spas_fourniture.id
               and spas_ligne_sortie.sortie_id=spas_sortie.id
               and spas_sortie.employe_id=spas_employe.id
               and spas_ligne_sortie.etat=%s
               group by spas_sortie.id,spas_sortie.date_s,spas_sortie.ref_s,spas_employe.nom,spas_employe.prenom
               order by spas_sortie.ref_s desc
            """

    lsors = Sortie.objects.raw(query, [active])
    paginator = Paginator(lsors, 10)
    page = request.GET.get('page')
    try:
        lsors = paginator.page(page)
    except PageNotAnInteger:
        lsors = paginator.page(1)
    except EmptyPage:
        lsors = paginator.page(paginator.num_pages)

    context = {'lsors': lsors,'paginator':paginator}
    return render(request, 'stock/fournitures/lsortie/lsortie.html', context)


# recherhe des fournitures sorties
def search_fourniture_sortie(request):

    if request.method == "GET" and 'date_fsort' in request.GET:
        date_fsort = request.GET.get('date_fsort')
        if (date_fsort != ''):
            fsorts = Ligne_sortie.objects.filter(sortie__date_s=date_fsort, etat='ACTIVE')
            context = {'date_fsort': date_fsort, 'fsorts': fsorts}
            return render(request, 'stock/fournitures/lsortie/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/fournitures/lsortie/search.html')


#Liste détaillé - fourniture sortie
def detail_list_lsortie(request, id):
    active = 'ACTIVE'
    query = """
                select spas_ligne_sortie.id,spas_fourniture.nom,spas_ligne_sortie.qte_s,spas_ligne_sortie.obs_ls,
                spas_sortie.ref_s,spas_sortie.date_s,concat(spas_employe.nom,' ',spas_employe.prenom) as np
                from spas_ligne_sortie,spas_fourniture,spas_sortie,spas_employe
                where spas_ligne_sortie.fourniture_id=spas_fourniture.id
                and spas_ligne_sortie.sortie_id=spas_sortie.id
                and spas_sortie.employe_id=spas_employe.id
                and spas_ligne_sortie.etat=%s
                and spas_ligne_sortie.sortie_id=%s
            """

    lsors = Ligne_sortie.objects.raw(query, [active, id])
    paginator = Paginator(lsors, 10)
    page = request.GET.get('page')
    try:
        lsors = paginator.page(page)
    except PageNotAnInteger:
        lsors = paginator.page(1)
    except EmptyPage:
        lsors = paginator.page(paginator.num_pages)

    context = {'lsors': lsors,'paginator':paginator}
    return render(request, 'stock/fournitures/lsortie/lsortie_detail.html', context)


#Création unique - fourniture sortie
def create_lsortie(request):
    form = Ligne_sortieForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lsortie')

    return render(request, 'stock/fournitures/lsortie/lsortie_form.html', {'form': form})


#Création multiple - fourniture sortie
def create_flsor(request):
    form = fLigne_sorForm(request.POST or None)
    en_cours = 'EN COURS'
    query = """
                select distinct spas_ligne_entree.id,spas_fourniture.nom,spas_entree.ref_e
                from spas_ligne_entree,spas_fourniture,spas_entree
                where spas_fourniture.id=spas_ligne_entree.fourniture_id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_ligne_entree.statut=%s
            """

    f_entrees = Ligne_entree.objects.raw(query,[en_cours])
    d = date.today().strftime("%d%m%Y")
    id_max = Sortie.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_sor = "SORTIE" + str(id_max) + str(d)
    if request.method=='POST':
        date_s = request.POST['date_s']
        ref_s = request.POST['ref_s']
        emp = request.POST['employe']
        four = request.POST.getlist('fourIds[]')#four represente la ligne achat ou il y a la fourniture acheté
        fournit_id = request.POST.getlist('FournitId[]') #fournit_id represente l'id de la fourniture en question
        qte = request.POST.getlist('qtefour[]')
        obs = request.POST.getlist('obs_ls[]')
        if (date_s and ref_s and emp):
            if (four and fournit_id):
                sort = Sortie.objects.create(ref_s=ref_s, date_s=date_s, employe=Employe.objects.get(pk=emp))
                sort_id = sort.id
                for i in range(len(four)):
                    four_sortie = Ligne_sortie.objects.create(sortie=Sortie.objects.get(pk=sort_id), lentree=Ligne_entree.objects.get(pk=four[i]), fourniture=Fourniture.objects.get(pk=fournit_id[i]), qte_s=qte[i], obs_ls=obs[i])
                    four_sortie_id = four_sortie.id
                    Mouvement.objects.create(date_m=date_s, ligne_sortie=Ligne_sortie.objects.get(pk=four_sortie_id), fourniture=Fourniture.objects.get(pk=fournit_id[i]), qte=qte[i], type='SORTIE')
                    qte_dis_e = list(Ligne_entree.objects.filter(id=four[i], statut='EN COURS', etat='ACTIVE').aggregate(
                        Sum('qte_e')).values())[0] or 0
                    qte_dis_s = \
                    list(Ligne_sortie.objects.filter(lentree_id=four[i], etat='ACTIVE').aggregate(Sum('qte_s')).values())[0] or 0
                    if (qte_dis_e == qte_dis_s):
                        Ligne_entree.objects.filter(id=four[i]).update(statut='EPUISEE')

                messages.success(request, "Enregistrement(s) effectué(s)")
                return redirect('list_lsortie')
            else:
                messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne de fourniture.")
                return render(request, 'stock/fournitures/lsortie/flsortie_form.html', {'form': form, 'ref': ref_sor,'f_entrees': f_entrees})
        else:
            messages.warning(request, "Svp, Veuillez remplir toutes les zones de saisies.")
            return render(request, 'stock/fournitures/lsortie/flsortie_form.html', {'form': form, 'ref': ref_sor,'f_entrees': f_entrees})

    return render(request, 'stock/fournitures/lsortie/flsortie_form.html', {'form': form,'ref':ref_sor,'f_entrees': f_entrees})


#Chargement automatique de l'id de la fourniture sur la page sortie
def load_fournit(request):
    entree_id = request.GET.get('entre_ref')
    fournit_id = get_object_or_404(Ligne_entree,id=entree_id)
    fId = fournit_id.fourniture.id
    return JsonResponse(fId, safe=False)


#MAJ - fourniture sortie
def update_lsortie(request, id):
    sor = get_object_or_404(Ligne_sortie,id=id)
    mouv = get_object_or_404(Mouvement,ligne_sortie_id=sor)
    form_s = Ligne_sortieForm(request.POST or None, instance=sor)

    if form_s.is_valid():
        # Mise a jour automatique des donnees de la table mouvement
        postf = form_s.save(commit=False)
        details = get_object_or_404(Sortie,ref_s=postf.sortie)
        date_sortie = details.date_s
        mouv.date_m = date_sortie
        mouv.fourniture = postf.fourniture
        mouv.qte = postf.qte_s
        # Fin de la Mise a jour automatique des donnees de la table mouvement
        postf.save()
        mouv.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_lsortie')

    return render(request, 'stock/fournitures/lsortie/lsortie_form.html', {'form': form_s, 'sor': sor})


#Suppression - fourniture sortie
def delete_lsortie(request, id):
    lsor = get_object_or_404(Ligne_sortie,id=id)
    mouv = get_object_or_404(Mouvement,ligne_sortie_id=lsor)

    if request.method == 'POST':
        lsor.etat = 'INACTIVE'
        mouv.etat = 'INACTIVE'
        lsor.save()
        mouv.save()
        # permet d'actualiser la ligne entree ou la fourniture est en cours au cas ou il serait préalablement epuisée dans
        # la table ligne entrée
        Ligne_entree.objects.filter(fourniture_id=lsor.fourniture_id).update(statut='EN COURS')
        messages.success(request, "Suppression effectuée")
        return redirect('list_lsortie')

    return render(request, 'stock/fournitures/lsortie/lsortie_sup_confirm.html', {'lsor': lsor})


#Chargement automatique de la quantité disponible de fourniture approvisionné sur la page de sortie des fournitures
def load_qte_fourniture(request):
    four_id = request.GET.get('achat_id')
    entree_id = request.GET.get('achat_id')
    fournit_id = get_object_or_404(Ligne_entree,id=entree_id)
    fId = fournit_id.fourniture.id

    qte_dis0 = list(Ligne_entree.objects.filter(id=four_id,statut='EN COURS',etat='ACTIVE').aggregate(Sum('qte_e')).values())[0] or 0
    qte_dis1 = list(Ligne_sortie.objects.filter(lentree_id=four_id,etat='ACTIVE').aggregate(Sum('qte_s')).values())[0] or 0
    qte_dis = qte_dis0 - qte_dis1
    
    return JsonResponse([fId, qte_dis], safe=False)


#Chargement automatique du service de l'utilisateur(employé) sur la page de sortie des fournitures et consommable
def load_service_utilisateur(request):
    emp_ref = request.GET.get('emp_ref')
    active = 'ACTIVE'
    query = """
               select spas_employe_service.id,spas_unite_organisation.nom_uo
               from spas_employe_service,spas_unite_organisation
               where spas_employe_service.u_orga_id=spas_unite_organisation.id
               and spas_employe_service.etat=%s
               and spas_employe_service.employe_id=%s
            """

    em_sers = Materiel.objects.raw(query, [active, emp_ref])
    return render(request, 'stock/fournitures/lsortie/emp_service.html', {'em_sers': em_sers})


# mouvement(appro-sortie) des fournitures
def list_mouv_appro_sortie(request):
    mouvsorss = Mouvement.objects.filter(etat='ACTIVE',fourniture_id__isnull=False,type='SORTIE').order_by('-id') # par ordre décroissant
    mouvsorsa = Mouvement.objects.filter(etat='ACTIVE', fourniture_id__isnull=False,type='APPRO').order_by('-id')  # par ordre décroissant


    context = {'mouvsorss': mouvsorss,'mouvsorsa': mouvsorsa,}
    return render(request, 'stock/fournitures/lsortie/mouvement_sortie.html', context)


# etat des mouvements de fournitures appro-sortie sur periode
def search_stock_periode(request):
    try:
        if request.method == "GET" and 'date_d' in request.GET and 'date_f' in request.GET and 'date_d' != '' and 'date_f' != '':
            date_d = request.GET.get('date_d')
            active = 'ACTIVE'
            date_f = request.GET.get('date_f')
            if(date_d<date_f):
                query = """ SELECT spas_fourniture.id AS id, spas_fourniture.nom, 
                            sum(case 
                                    when spas_mouvement.date_m < %s 
                                    then case spas_mouvement.type when 'SORTIE' then -1 else 1 end
                                    else 0 
                                end * qte) AS st_init,
                            sum(case
                                    when spas_mouvement.date_m BETWEEN %s AND %s
                                    AND spas_mouvement.type = 'APPRO' then qte
                                    else 0 
                            end) AS qt_e,
                            sum(case 
                                    when spas_mouvement.date_m BETWEEN %s AND %s 
                                    AND spas_mouvement.type = 'SORTIE' then qte
                                    else 0 
                                end) AS qt_s, 
                            sum(case spas_mouvement.type when 'SORTIE' then -1 else 1 end * qte) AS st_fin
                            FROM spas_mouvement,spas_fourniture
                            WHERE spas_mouvement.fourniture_id=spas_fourniture.id 
                            AND spas_mouvement.etat <= %s 
                            AND spas_mouvement.date_m <= %s 
                            GROUP BY spas_fourniture.id
                            ORDER BY spas_fourniture.nom 
                        """

                sit_p = Fourniture.objects.raw(query, [date_d, date_d, date_f, date_d, date_f, active,date_f])

                context = {'sit_p': sit_p, 'date_d': date_d, 'date_f': date_f}
                return render(request, 'etat/stock/situation_periode.html', context)
            else:
                messages.warning(request, "Veuillez saisir correctement les dates.")
                return render(request, 'etat/stock/situation_periode.html', {'date_d': date_d, 'date_f': date_f})
        else:
            return render(request, 'etat/stock/situation_periode.html')
    except:
        return HttpResponse("505 Not Found")
    

# etat situation periode fourniture - pdf
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and 'date_d' in request.GET and 'date_f' in request.GET:
            date_d = request.GET.get('date_d')
            active = 'ACTIVE'
            date_f = request.GET.get('date_f')
            if (date_d < date_f):
                query = """ SELECT spas_fourniture.id AS id, spas_fourniture.nom, 
                            sum(case 
                                    when spas_mouvement.date_m < %s 
                                    then case spas_mouvement.type when 'SORTIE' then -1 else 1 end
                                    else 0 
                                end * qte) AS st_init,
                            sum(case
                                    when spas_mouvement.date_m BETWEEN %s AND %s
                                     AND spas_mouvement.type = 'APPRO' then qte
                                    else 0 
                               end) AS qt_e,
                            sum(case 
                                    when spas_mouvement.date_m BETWEEN %s AND %s 
                                     AND spas_mouvement.type = 'SORTIE' then qte
                                    else 0 
                                end) AS qt_s, 
                            sum(case spas_mouvement.type when 'SORTIE' then -1 else 1 end * qte) AS st_fin
                            FROM spas_mouvement,spas_fourniture
                            WHERE spas_mouvement.fourniture_id=spas_fourniture.id 
                            AND spas_mouvement.etat <= %s 
                            AND spas_mouvement.date_m <= %s 
                            GROUP BY spas_fourniture.id
                            ORDER BY spas_fourniture.nom
                        """

                sit_p = Fourniture.objects.raw(query, [date_d, date_d, date_f, date_d, date_f, active, date_f])
                data = {
                    'today': datetime.date.today(),
                    'date_d':date_d,
                    'date_f':date_f,
                    'fours': sit_p,
                }
                pdf = render_to_pdf('etat/stock/sit_periode.html', data)
                return HttpResponse(pdf, content_type='application/pdf')
        else:
            messages.warning(request, "Aucune donnée à exporter :-)")
            return render(request, 'etat/stock/situation_periode.html')


# etat situation commande en cours des fournitures
def search_stock_cmd_cours(request):
    active = 'ACTIVE'
    status = 'EN COURS'

    query = """ select spas_ligne_commande.id,spas_commande.date_c,spas_commande.ref_c,spas_fourniture.nom,
                spas_type.nom_type,spas_ligne_commande.qte_c,
                concat(round(spas_ligne_commande.qte_c/spas_fourniture.base),' ',spas_fourniture.mesure,'(S)') as qte_mesure
                from spas_ligne_commande,spas_commande,spas_fourniture,spas_type
                where spas_ligne_commande.fourniture_id=spas_fourniture.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_fourniture.type_id=spas_type.id
                and spas_ligne_commande.etat = %s
                and spas_ligne_commande.statut = %s
            """

    cmd_cours = Ligne_commande.objects.raw(query, [active,status])
    context = {'cmd_cours': cmd_cours}
    return render(request, 'etat/stock/commande_en_cours.html', context)


# etat situation commande en cours des fournitures - pdf
class Commande_cours(View):
    def get(self, request, *args, **kwargs):
        active = 'ACTIVE'
        status = 'EN COURS'

        query = """ select spas_ligne_commande.id,spas_commande.date_c,spas_commande.ref_c,spas_fourniture.nom,
                    spas_type.nom_type,spas_ligne_commande.qte_c,
                    concat(round(spas_ligne_commande.qte_c/spas_fourniture.base),' ',spas_fourniture.mesure,'(S)') as qte_mesure
                    from spas_ligne_commande,spas_commande,spas_fourniture,spas_type
                    where spas_ligne_commande.fourniture_id=spas_fourniture.id
                    and spas_ligne_commande.commande_id=spas_commande.id
                    and spas_fourniture.type_id=spas_type.id
                    and spas_ligne_commande.etat = %s
                    and spas_ligne_commande.statut = %s 
                """
        cmd_cours = Ligne_commande.objects.raw(query, [active, status])
        data = {
            'today': datetime.date.today(),
            'fours': cmd_cours,
        }
        pdf = render_to_pdf('etat/stock/cmd_cours.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

### Partie consommable

#Liste - consommable
@login_required
def list_consommable(request):
    cons = Consommable.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(cons, 10)
    page = request.GET.get('page')
    try:
        cons = paginator.page(page)
    except PageNotAnInteger:
        cons = paginator.page(1)
    except EmptyPage:
        cons = paginator.page(paginator.num_pages)

    context = {'cons': cons,'paginator':paginator}
    return render(request, 'stock/consommables/consommable/consommable.html', context)


#Création - consommable
def create_consommable(request):
    form = ConsommableForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_consommable')

    return render(request, 'stock/consommables/consommable/consommable_form.html', {'form': form})


#MAJ - consommable
def update_consommable(request, id):
    cons = get_object_or_404(Consommable,id=id)
    form = ConsommableForm(request.POST or None, instance=cons)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_consommable')

    return render(request, 'stock/consommables/consommable/consommable_form.html', {'form': form})


#Suppression - consommable
def delete_consommable(request, id):
    cons = get_object_or_404(Consommable,id=id)

    if request.method == 'POST':
        cons.etat = 'INACTIVE'
        cons.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_consommable')

    return render(request, 'stock/consommables/consommable/consommable_sup_confirm.html', {'cons': cons})

# Commande pour consommable (consommable_commande)

#Liste - consommable commandé
def list_lccommande(request):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_commande.id,spas_commande.date_c,spas_commande.ref_c,count(spas_ligne_commande.consommable_id) as nbcons,
                sum(spas_ligne_commande.qte_c) as qte_total,sum(spas_ligne_commande.prix_c) as prix_total
                from spas_ligne_commande,spas_commande,spas_consommable
                where spas_ligne_commande.consommable_id=spas_consommable.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                group by spas_commande.id,spas_commande.date_c,spas_commande.ref_c
                order by spas_commande.ref_c desc
            """

    lccoms = Commande.objects.raw(query, [active, en_cours])
    #lcoms = Ligne_commande.objects.order_by('-id')  par ordre décroissant
    paginator = Paginator(lccoms, 10)
    page = request.GET.get('page')
    try:
        lccoms = paginator.page(page)
    except PageNotAnInteger:
        lccoms = paginator.page(1)
    except EmptyPage:
        lccoms = paginator.page(paginator.num_pages)

    context = {'lccoms': lccoms,'paginator':paginator}
    return render(request, 'stock/consommables/lccommande/lccommande.html', context)


# recherhe des consommables commandés
def search_consommable_commande(request):

    if request.method == "GET" and 'date_ccmd' in request.GET:
        date_ccmd = request.GET.get('date_ccmd')
        if (date_ccmd != ''):
            ccmds = Ligne_commande.objects.filter(commande__date_c=date_ccmd, etat='ACTIVE')
            context = {'date_ccmd': date_ccmd, 'ccmds': ccmds}
            return render(request, 'stock/consommables/lccommande/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/consommables/lccommande/search.html')


#Liste détaillé - consommable commandé
def detail_lccommande(request, id):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_commande.id,spas_consommable.nom,spas_ligne_commande.qte_c,spas_ligne_commande.prix_c,
                spas_commande.ref_c,spas_commande.date_c,spas_ligne_commande.obs_c
                from spas_ligne_commande,spas_commande,spas_consommable
                where spas_ligne_commande.consommable_id=spas_consommable.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_commande.id=%s
            """

    lccoms = Ligne_commande.objects.raw(query, [active, en_cours, id])
    paginator = Paginator(lccoms, 10)
    page = request.GET.get('page')
    try:
        lccoms = paginator.page(page)
    except PageNotAnInteger:
        lccoms = paginator.page(1)
    except EmptyPage:
        lccoms = paginator.page(paginator.num_pages)

    context = {'lccoms': lccoms,'paginator':paginator}
    return render(request, 'stock/consommables/lccommande/lccommande_detail.html', context)


#Création unique - consommable commandé
def create_lccommande(request):
    form = Ligne_consommable_commandeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lccommande')

    return render(request, 'stock/consommables/lccommande/lccommande_form.html', {'form': form})


#Création multiple - consommable commandé
def create_clcom(request):
    form = cLigne_comForm(request.POST or None)
    d = date.today().strftime("%d%m%Y")
    id_max = Commande.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_com = "CMD0" + str(id_max) + str(d)
    if request.method=='POST':
        date_com = request.POST['date_c']
        ref_com = request.POST['ref_c']
        cons = request.POST.getlist('fourIds[]')
        qte = request.POST.getlist('qtefour[]')
        obs = request.POST.getlist('obs_c[]')
        prix = request.POST.getlist('prices[]')
        if (cons):
            com = Commande.objects.create(ref_c=ref_com, date_c=date_com)
            commande_id = com.id
            for i in range(len(cons)):
                Ligne_commande.objects.create(commande=Commande.objects.get(pk=commande_id), consommable=Consommable.objects.get(pk=cons[i]), qte_c=qte[i], prix_c=prix[i], obs_c=obs[i])

            messages.success(request, "Enregistrement(s) effectué(s)")
            return redirect('list_lccommande')
        else:
            messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne commande de consommable.")
            return render(request, 'stock/consommables/lccommande/lccom_form.html', {'form': form, 'ref': ref_com})

    return render(request, 'stock/consommables/lccommande/lccom_form.html', {'form': form,'ref':ref_com})


#MAJ - consommable commandé
def update_lccommande(request, id):
    com = get_object_or_404(Ligne_commande,id=id)
    form = Ligne_consommable_commandeForm(request.POST or None, instance=com)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_lccommande')

    return render(request, 'stock/consommables/lccommande/lccommande_form.html', {'form': form})


#Suppression - consommable commandé
def delete_lccommande(request, id):
    lccom = get_object_or_404(Ligne_commande,id=id)

    if request.method == 'POST':
        lccom.etat = 'INACTIVE'
        lccom.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_lccommande')

    return render(request, 'stock/consommables/lccommande/lccommande_sup_confirm.html', {'lccom': lccom})

# Approvisionnement pour consommable (consommable_entree).

#Liste - consommable approvisionné
def list_lcentree(request):
    #lcents = Ligne_entree.objects.filter(etat='ACTIVE', consommable__isnull=False).order_by('-id') # par ordre décroissant
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
            select spas_entree.id,spas_entree.date_e,spas_entree.ref_e,spas_fournisseur.nom as nomf,
            count(spas_ligne_entree.consommable_id) as nbcon, sum(spas_ligne_entree.qte_e) as qte_total,
            sum(spas_ligne_entree.prix_e) as prix_total
            from spas_ligne_entree,spas_entree,spas_consommable,spas_fournisseur
            where spas_ligne_entree.consommable_id=spas_consommable.id
            and spas_ligne_entree.entree_id=spas_entree.id
            and spas_entree.fournisseur_id=spas_fournisseur.id
            and spas_ligne_entree.etat=%s
            and spas_ligne_entree.statut=%s
            group by spas_entree.id,spas_entree.date_e,spas_entree.ref_e,spas_fournisseur.nom
            order by spas_entree.ref_e desc
        """

    lcents = Entree.objects.raw(query, [active, en_cours])
    paginator = Paginator(lcents, 10)
    page = request.GET.get('page')
    try:
        lcents = paginator.page(page)
    except PageNotAnInteger:
        lcents = paginator.page(1)
    except EmptyPage:
        lcents = paginator.page(paginator.num_pages)

    context = {'lcents': lcents,'paginator':paginator}
    return render(request, 'stock/consommables/lcentree/lentree.html', context)


# recherhe des consommables entrées
def search_consommable_entree(request):

    if request.method == "GET" and 'date_cent' in request.GET:
        date_cent = request.GET.get('date_cent')
        if (date_cent != ''):
            cents = Ligne_entree.objects.filter(entree__date_e=date_cent, etat='ACTIVE')
            context = {'date_cent': date_cent, 'cents': cents}
            return render(request, 'stock/consommables/lcentree/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/consommables/lcentree/search.html')


#Liste détaillé - consommable approvisionné
def detail_list_lcentree(request, id):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_entree.id,spas_consommable.nom,spas_fournisseur.nom as nomf,spas_ligne_entree.qte_e,
                spas_ligne_entree.prix_e,spas_entree.ref_e,spas_entree.date_e
                from spas_ligne_entree,spas_consommable,spas_entree,spas_fournisseur
                where spas_ligne_entree.consommable_id=spas_consommable.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_entree.fournisseur_id=spas_fournisseur.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
                and spas_ligne_entree.entree_id=%s
            """

    lcents = Ligne_entree.objects.raw(query, [active, en_cours, id])
    paginator = Paginator(lcents, 10)
    page = request.GET.get('page')
    try:
        lcents = paginator.page(page)
    except PageNotAnInteger:
        lcents = paginator.page(1)
    except EmptyPage:
        lcents = paginator.page(paginator.num_pages)

    context = {'lcents': lcents,'paginator':paginator}
    return render(request, 'stock/consommables/lcentree/lentree_detail.html', context)


#Création unique - consommable approvisionné
def create_lcentree(request):
    form = Ligne_entreecForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lcentree')

    return render(request, 'stock/consommables/lcentree/lentree_form.html', {'form': form})


#Chargement de la liste déroulante des consommable commandés sur la page des consommable approvisionné
def load_consommable_cmd(request):
    cmd_ref = request.GET.get('cmd_ref')
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
               select spas_ligne_commande.id, spas_ligne_commande.consommable_id,spas_consommable.nom,spas_ligne_commande.qte_c,
               spas_ligne_commande.prix_c
               from spas_ligne_commande,spas_commande,spas_consommable
               where spas_ligne_commande.commande_id=spas_commande.id
               and spas_ligne_commande.consommable_id=spas_consommable.id
               and spas_ligne_commande.etat=%s
               and spas_ligne_commande.statut=%s
               and spas_commande.ref_c=%s
            """

    c_cmds = Ligne_commande.objects.raw(query, [active, en_cours,cmd_ref])
    return render(request, 'stock/consommables/lcentree/consommable_cmd.html', {'c_cmds': c_cmds})


#Création multiple - consommable approvisionné
def create_clent(request):
    form = cLentreForm(request.POST or None)
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select distinct spas_commande.id,spas_commande.ref_c
                from spas_ligne_commande,spas_commande
                where spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_ligne_commande.consommable_id is not null 
                order by spas_commande.ref_c desc
            """

    commande = Commande.objects.raw(query, [active, en_cours])
    d = date.today().strftime("%d%m%Y")
    id_max = Entree.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_ent = "APPRO" + str(id_max) + str(d)
    if request.method=='POST':
        date_e = request.POST['date_e']
        ref_e = request.POST['ref_e']
        fournis = request.POST['fournisseur']
        employe = request.user.id
        con = request.POST.getlist('fourIds[]') #con represente la ligne commande ou il y a le consommable cmdé
        consommable_id = request.POST.getlist('ConId[]') #consommable_id represente l'id du consommable en question
        qte = request.POST.getlist('qtefour[]')
        prix = request.POST.getlist('prices[]')
        if (date_e and ref_e and fournis and employe):
            if (con and consommable_id):
                ent = Entree.objects.create(ref_e=ref_e, date_e=date_e, fournisseur=Fournisseur.objects.get(pk=fournis),employe=MyUser.objects.get(pk=employe))
                entree_id = ent.id
                for i in range(len(con)):
                    con_entree = Ligne_entree.objects.create(entree=Entree.objects.get(pk=entree_id), commande=Ligne_commande.objects.get(pk=con[i]), consommable=Consommable.objects.get(pk=consommable_id[i]), qte_e=qte[i], prix_e=prix[i])
                    con_entree_id = con_entree.id
                    Mouvement.objects.create(date_m=date_e, ligne_appro=Ligne_entree.objects.get(pk=con_entree_id), consommable=Consommable.objects.get(pk=consommable_id[i]), qte=qte[i], type='APPRO')
                    Ligne_commande.objects.filter(id=con[i]).update(statut='LIVREE')

                messages.success(request, "Enregistrement(s) effectué(s)")
                return redirect('list_lcentree')
            else:
                messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne de consommable.")
                return render(request, 'stock/consommables/lcentree/clentre_form.html', {'form': form, 'ref': ref_ent,'commande':commande})
        else:
            messages.warning(request, "Svp, Veuillez remplir toutes les zones de saisies.")
            return render(request, 'stock/consommables/lcentree/clentre_form.html', {'form': form, 'ref': ref_ent,'commande':commande})

    return render(request, 'stock/consommables/lcentree/clentre_form.html', {'form': form,'ref':ref_ent,'commande':commande})


#Chargement automatique de l'id du consommable sur la page entree(appro)
def load_consommable(request):
    com_id = request.GET.get('ligne_commande')
    con_id = get_object_or_404(Ligne_commande,id=com_id)
    cId = con_id.consommable.id
    return JsonResponse(cId, safe=False)


#MAJ - consommable approvisionné
def update_lcentree(request, id):
    ent = get_object_or_404(Ligne_entree,id=id)
    mouv = get_object_or_404(Mouvement,ligne_appro_id=ent)
    form = Ligne_entreecForm(request.POST or None, instance=ent)

    #verification si la livraison est déja utilisé(présent dans la table sortie)
    ent_utilise = list(Ligne_sortie.objects.filter(lentree_id=id,etat='ACTIVE').aggregate(Sum('lentree')).values())[0] or 0

    if form.is_valid():
        if ent_utilise == 0:
            postc = form.save(commit=False)
            # Mise a jour automatique des donnees de la table mouvement
            details = get_object_or_404(Entree,ref_e=postc.entree)
            date_entree = details.date_e
            mouv.date_m = date_entree
            mouv.consommable = postc.consommable
            mouv.qte = postc.qte_e
            # Fin de la Mise a jour automatique des donnees de la table mouvement
            postc.save()
            mouv.save()
            messages.success(request, "Modification effectuée")
            return redirect('list_lcentree')
        else:
            messages.success(request, "Modification impossible, la livraison est utilisation.")
            return redirect('list_lcentree')

    return render(request, 'stock/consommables/lcentree/lentree_form.html', {'form': form, 'ent': ent})


#Suppression - consommable approvisionné
def delete_lcentree(request, id):
    lent = get_object_or_404(Ligne_entree,id=id)
    mouv = get_object_or_404(Mouvement,ligne_appro_id=lent)

    #verification si la livraison est déja utilisé(présent dans la table sortie)
    lent_utilise = list(Ligne_sortie.objects.filter(lentree_id=id,etat='ACTIVE').aggregate(Sum('lentree')).values())[0] or 0

    if request.method == 'POST':
        if lent_utilise == 0:
            # permet d'actualiser la ligne commande ou le consommable est en cours au cas ou il serait préalablement livrée dans
            # la table ligne commande
            commande_id = lent.commande_id
            Ligne_commande.objects.filter(id=commande_id).update(statut='EN COURS')
            lent.etat = 'INACTIVE'
            mouv.etat = 'INACTIVE'
            lent.save()
            mouv.save()
            messages.success(request, "Suppression effectuée")
            return redirect('list_lcentree')
        else:
            messages.success(request, "Suppression impossible, la livraison est utilisation.")
            return redirect('list_lcentree')

    return render(request, 'stock/consommables/lcentree/lentree_sup_confirm.html', {'lent': lent})


# Sortie pour consommable (consommable_sortie).


#Liste - consommable sortie
def list_lcsortie(request):
    #lcsors = Ligne_sortie.objects.filter(etat='ACTIVE',consommable__isnull=False).order_by('-id') # par ordre décroissant
    active = 'ACTIVE'
    query = """
                select spas_sortie.id,spas_sortie.date_s,spas_sortie.ref_s,count(spas_ligne_sortie.consommable_id) as nbcon,
                sum(spas_ligne_sortie.qte_s) as qte_total,concat(spas_employe.nom,' ',spas_employe.prenom) as np
                from spas_ligne_sortie,spas_sortie,spas_consommable,spas_employe
                where spas_ligne_sortie.consommable_id=spas_consommable.id
                and spas_ligne_sortie.sortie_id=spas_sortie.id
                and spas_sortie.employe_id=spas_employe.id
                and spas_ligne_sortie.etat=%s
                group by spas_sortie.id,spas_sortie.date_s,spas_sortie.ref_s,spas_employe.nom,spas_employe.prenom
                order by spas_sortie.ref_s desc
            """

    lcsors = Sortie.objects.raw(query, [active])

    paginator = Paginator(lcsors, 10)
    page = request.GET.get('page')
    try:
        lcsors = paginator.page(page)
    except PageNotAnInteger:
        lcsors = paginator.page(1)
    except EmptyPage:
        lcsors = paginator.page(paginator.num_pages)

    context = {'lcsors': lcsors,'paginator':paginator}
    return render(request, 'stock/consommables/lcsortie/lcsortie.html', context)


#Liste détaillé - consommable sortie
def detail_list_lcsortie(request, id):
    active = 'ACTIVE'
    query = """
            select spas_ligne_sortie.id,spas_consommable.nom,spas_ligne_sortie.qte_s,spas_ligne_sortie.obs_ls,spas_sortie.ref_s,
            spas_sortie.date_s,concat(spas_employe.nom,' ',spas_employe.prenom) as np
            from spas_ligne_sortie,spas_consommable,spas_sortie,spas_employe
            where spas_ligne_sortie.consommable_id=spas_consommable.id
            and spas_ligne_sortie.sortie_id=spas_sortie.id
            and spas_sortie.employe_id=spas_employe.id
            and spas_ligne_sortie.etat=%s
            and spas_ligne_sortie.sortie_id=%s
        """

    lcsors = Ligne_sortie.objects.raw(query, [active, id])
    paginator = Paginator(lcsors, 10)
    page = request.GET.get('page')
    try:
        lcsors = paginator.page(page)
    except PageNotAnInteger:
        lcsors = paginator.page(1)
    except EmptyPage:
        lcsors = paginator.page(paginator.num_pages)

    context = {'lcsors': lcsors,'paginator':paginator}
    return render(request, 'stock/consommables/lcsortie/lcsortie_detail.html', context)


#Création unique - consommable sortie
def create_lcsortie(request):
    form = Ligne_sortiecForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lcsortie')

    return render(request, 'stock/consommables/lcsortie/lcsortie_form.html', {'form': form})


#Création multiple - consommable sortie
def create_clsor(request):
    form = CLigne_sorForm(request.POST or None)
    en_cours = 'EN COURS'
    query = """
                select distinct spas_ligne_entree.id,spas_consommable.nom,spas_entree.ref_e
                from spas_ligne_entree,spas_consommable,spas_entree
                where spas_consommable.id=spas_ligne_entree.consommable_id
                and spas_entree.id=spas_ligne_entree.entree_id
                and spas_ligne_entree.statut=%s
            """

    c_entrees = Ligne_entree.objects.raw(query, [en_cours])
    d = date.today().strftime("%d%m%Y")
    id_max = Sortie.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_sor = "SORTIE" + str(id_max) + str(d)
    if request.method=='POST':
        date_s = request.POST['date_s']
        ref_s = request.POST['ref_s']
        emp = request.POST['employe']
        con = request.POST.getlist('fourIds[]')#con represente la ligne commande ou il y a le consommable acheté
        consommable_id = request.POST.getlist('ConId[]') #consommable_id represente l'id du consommable en question
        qte = request.POST.getlist('qtefour[]')
        obs = request.POST.getlist('obs_ls[]')
        if(date_s and ref_s and emp):
            if (con and consommable_id):
                sort = Sortie.objects.create(ref_s=ref_s, date_s=date_s, employe=Employe.objects.get(pk=emp))
                sort_id = sort.id
                for i in range(len(con)):
                    con_sortie = Ligne_sortie.objects.create(sortie=Sortie.objects.get(pk=sort_id), lentree=Ligne_entree.objects.get(pk=con[i]), consommable=Consommable.objects.get(pk=consommable_id[i]), qte_s=qte[i], obs_ls=obs[i])
                    con_sortie_id = con_sortie.id
                    Mouvement.objects.create(date_m=date_s, ligne_sortie=Ligne_sortie.objects.get(pk=con_sortie_id), consommable=Consommable.objects.get(pk=consommable_id[i]), qte=qte[i], type='SORTIE')
                    qte_dis_e = list(Ligne_entree.objects.filter(id=con[i], statut='EN COURS', etat='ACTIVE').aggregate(
                        Sum('qte_e')).values())[0] or 0
                    qte_dis_s = \
                        list(Ligne_sortie.objects.filter(lentree_id=con[i], etat='ACTIVE').aggregate(Sum('qte_s')).values())[
                            0] or 0
                    if (qte_dis_e == qte_dis_s):
                        Ligne_entree.objects.filter(id=con[i]).update(statut='EPUISEE')

                messages.success(request, "Enregistrement(s) effectué(s)")
                return redirect('list_lcsortie')
            else:
                messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne de consommable.")
                return render(request, 'stock/consommables/lcsortie/clsortie_form.html', {'form': form, 'ref': ref_sor, 'c_entrees':c_entrees})
        else:
            messages.warning(request, "Svp, Veuillez remplir toutes les zones de saisies.")
            return render(request, 'stock/consommables/lcsortie/clsortie_form.html', {'form': form, 'ref': ref_sor, 'c_entrees':c_entrees})

    return render(request, 'stock/consommables/lcsortie/clsortie_form.html', {'form': form,'ref':ref_sor, 'c_entrees':c_entrees})


#MAJ - consommable sortie
def update_lcsortie(request, id):
    sor = get_object_or_404(Ligne_sortie,id=id)
    mouv = get_object_or_404(Mouvement,ligne_sortie_id=sor)
    form_c = Ligne_sortiecForm(request.POST or None, instance=sor)

    if form_c.is_valid():
        postc = form_c.save(commit=False)
        # Mise a jour automatique des donnees de la table mouvement
        details = get_object_or_404(Sortie,ref_s=postc.sortie)
        date_sortie = details.date_s
        mouv.date_m = date_sortie
        mouv.consommable = postc.consommable
        mouv.qte = postc.qte_s
        # Fin de la Mise a jour automatique des donnees de la table mouvement
        postc.save()
        mouv.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_lcsortie')

    return render(request, 'stock/consommables/lcsortie/lcsortie_form.html', {'form': form_c, 'sor': sor})


#Suppression - consommable sortie
def delete_lcsortie(request, id):
    lsor = get_object_or_404(Ligne_sortie,id=id)
    mouv = get_object_or_404(Mouvement,ligne_sortie_id=lsor)

    if request.method == 'POST':
        lsor.etat = 'INACTIVE'
        mouv.etat = 'INACTIVE'
        lsor.save()
        mouv.save()
        # permet d'actualiser la ligne entree ou le consommable est en cours au cas ou il serait préalablement epuisée
        Ligne_entree.objects.filter(consommable_id=lsor.consommable_id).update(statut='EN COURS')
        messages.success(request, "Suppression effectuée")
        return redirect('list_lcsortie')

    return render(request, 'stock/consommables/lcsortie/lcsortie_sup_confirm.html', {'lsor': lsor})


# recherhe des consommables sorties
def search_consommable_sortie(request):

    if request.method == "GET" and 'date_csort' in request.GET:
        date_csort = request.GET.get('date_csort')
        if (date_csort != ''):
            csorts = Ligne_sortie.objects.filter(sortie__date_s=date_csort, etat='ACTIVE')
            context = {'date_csort': date_csort, 'csorts': csorts}
            return render(request, 'stock/consommables/lcsortie/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'stock/consommables/lcsortie/search.html')


#Chargement automatique de la quantité disponible de consommable approvisionné sur la page de sortie des consommables
def load_qte_consommable(request):
    con_id = request.GET.get('consommable')
    entree_id = request.GET.get('consommable')
    cons_id = get_object_or_404(Ligne_entree,id=entree_id)
    cId = cons_id.consommable.id

    qte_disc0 = list(Ligne_entree.objects.filter(id=con_id,statut='EN COURS',etat='ACTIVE').aggregate(Sum('qte_e')).values())[0] or 0
    qte_disc1 = list(Ligne_sortie.objects.filter(lentree_id=con_id,etat='ACTIVE').aggregate(Sum('qte_s')).values())[0] or 0
    qte_disc = qte_disc0 - qte_disc1
    
    return JsonResponse([cId, qte_disc], safe=False)



# mouvement(appro-sortie) des consommables
def list_mouv_con_appro_sortie(request):
    mouvsors = Mouvement.objects.filter(consommable_id__isnull=False).order_by('-id') # par ordre décroissant
    paginator = Paginator(mouvsors, 10)
    page = request.GET.get('page')
    try:
        mouvsors = paginator.page(page)
    except PageNotAnInteger:
        mouvsors = paginator.page(1)
    except EmptyPage:
        mouvsors = paginator.page(paginator.num_pages)

    context = {'mouvsors': mouvsors,'paginator':paginator}
    return render(request, 'stock/consommables/lcsortie/mouvement_sortie.html', context)


### Gestion du Patrimoine

#Liste - modele materiel
@login_required
def list_modele(request):
    modmats = Modele_mat.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(modmats, 10)
    page = request.GET.get('page')
    try:
        modmats = paginator.page(page)
    except PageNotAnInteger:
        modmats = paginator.page(1)
    except EmptyPage:
        modmats = paginator.page(paginator.num_pages)

    context = {'modmats': modmats,'paginator':paginator}
    return render(request, 'patrimoine/modele/modele.html', context)


#Création - modele materiel
def create_modele(request):
    form = Modele_matForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_modele')

    return render(request, 'patrimoine/modele/modele_form.html', {'form': form})


#MAJ - modele materiel
def update_modele(request, id):
    modmat = get_object_or_404(Modele_mat,id=id)
    form = Modele_matForm(request.POST or None, instance=modmat)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_modele')

    return render(request, 'patrimoine/modele/modele_form.html', {'form': form})


#Suppression - modele materiel
def delete_modele(request, id):
    modmat = get_object_or_404(Modele_mat,id=id)

    if request.method == 'POST':
        modmat.etat = 'INACTIVE'
        modmat.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_modele')

    return render(request, 'patrimoine/modele/modele_sup_confirm.html', {'modmat': modmat})


#Test
def test(request):
    return render(request, 'registration/base.html')


#Test
def demoses(request):
    if request.method=='POST':
        nom = request.POST['nom'],
        #type = request.POST['type'],
        a = Type(nom_type=nom)
        a.save()
        return HttpResponse('Ok')


#Liste - materiel
@login_required
def list_materiel(request):
    materiels = Materiel.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(materiels, 10)
    page = request.GET.get('page')
    try:
        materiels = paginator.page(page)
    except PageNotAnInteger:
        materiels = paginator.page(1)
    except EmptyPage:
        materiels = paginator.page(paginator.num_pages)

    context = {'materiels': materiels,'paginator':paginator}
    return render(request, 'patrimoine/materiel/materiel.html', context)


#Création - materiel
def create_materiel(request):
    form = MaterielForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_materiel')

    return render(request, 'patrimoine/materiel/materiel_form.html', {'form': form})


#MAJ - materiel
def update_materiel(request, id):
    materiel = get_object_or_404(Materiel,id=id)
    form = MaterielForm(request.POST or None, instance=materiel)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_materiel')

    return render(request, 'patrimoine/materiel/materiel_form.html', {'form': form})


#Suppression - materiel
def delete_materiel(request, id):
    materiel = get_object_or_404(Materiel,id=id)

    if request.method == 'POST':
        materiel.etat = 'INACTIVE'
        materiel.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_materiel')

    return render(request, 'patrimoine/materiel/materiel_sup_confirm.html', {'materiel': materiel})


# recherhe des materiels
def search_materiel(request):

    if request.method == "GET" and 'req_m' in request.GET:
        req_m = request.GET.get('req_m')
        if (req_m != ''):
            mats = Materiel.objects.filter(nom__icontains=req_m, etat='ACTIVE')
            context = {'req_m': req_m, 'mats': mats}
            return render(request, 'materiel/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'patrimoine/materiel/search.html')


#Liste - affectation
@login_required
def list_affectation(request):
    affs = Affectation.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant

    paginator = Paginator(affs, 10)
    page = request.GET.get('page')
    try:
        affs = paginator.page(page)
    except PageNotAnInteger:
        affs = paginator.page(1)
    except EmptyPage:
        affs = paginator.page(paginator.num_pages)

    context = {'affs': affs,'paginator':paginator}
    return render(request, 'patrimoine/affectation/affectation.html', context)


# recherhe des materiels affectes (materiel sortie)
def search_materiel_affecte(request):

    if request.method == "GET" and 'req_maf' in request.GET:
        req_maf = request.GET.get('req_maf')
        if (req_maf != ''):
            mafs = Affectation.objects.filter(materiel__nom__icontains=req_maf, etat='ACTIVE')
            context = {'req_maf': req_maf, 'mafs': mafs}
            return render(request, 'patrimoine/affectation/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'patrimoine/affectation/search.html')


#Création - affectation
def create_affectation(request):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_materiel.id,spas_materiel.nom
                from spas_ligne_entree,spas_materiel,spas_entree
                where spas_ligne_entree.materiel_id=spas_materiel.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
            """

    mat = Materiel.objects.raw(query, [active, en_cours])
    form = AffectationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_affectation')

    return render(request, 'patrimoine/affectation/affectation_form.html', {'form': form,'mat': mat})


#MAJ - affectation
def update_affectation(request, id):
    aff = get_object_or_404(Affectation,id=id)
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_materiel.id,spas_materiel.nom
                from spas_ligne_entree,spas_materiel,spas_entree
                where spas_ligne_entree.materiel_id=spas_materiel.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
                and spas_materiel.id=%s
            """

    mat = Materiel.objects.raw(query, [active, en_cours,aff.materiel.id])
    form = AffectationForm(request.POST or None, instance=aff)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_affectation')

    return render(request, 'patrimoine/affectation/affectation_uform.html', {'form': form,'mat': mat})


#Suppression - affectation
def delete_affectation(request, id):
    aff = get_object_or_404(Affectation,id=id)

    if request.method == 'POST':
        aff.etat = 'INACTIVE'
        aff.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_affectation')

    return render(request, 'patrimoine/affectation/affectation_sup_confirm.html', {'aff': aff})


#Liste - maintenance 
@login_required
def list_maintenance(request):
    mains = Maintenance.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(mains, 10)
    page = request.GET.get('page')
    try:
        mains = paginator.page(page)
    except PageNotAnInteger:
        mains = paginator.page(1)
    except EmptyPage:
        mains = paginator.page(paginator.num_pages)

    context = {'mains': mains,'paginator':paginator}
    return render(request, 'patrimoine/maintenance/maintenance.html', context)


#Création - maintenance
def create_maintenance(request):
    form = MaintenanceForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_maintenance')

    return render(request, 'patrimoine/maintenance/maintenance_form.html', {'form': form})


#MAJ - maintenance
def update_maintenance(request, id):
    main = get_object_or_404(Maintenance,id=id)
    form = MaintenanceForm(request.POST or None, instance=main)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_maintenance')

    return render(request, 'patrimoine/maintenance/maintenance_form.html', {'form': form})


#Suppression - maintenance
def delete_maintenance(request, id):
    main = get_object_or_404(Maintenance,id=id)

    if request.method == 'POST':
        main.etat = 'INACTIVE'
        main.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_maintenance')

    return render(request, 'patrimoine/maintenance/maintenance_sup_confirm.html', {'main': main})

# Commande pour les materiels (materiel_commande)

#Liste - materiel commandé
def list_lmcommande(request):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_commande.id,spas_commande.date_c,spas_commande.ref_c,count(spas_ligne_commande.materiel_id) as nbmat,
                sum(spas_ligne_commande.qte_c) as qte_total,sum(spas_ligne_commande.prix_c) as prix_total
                from spas_ligne_commande,spas_commande,spas_materiel
                where spas_ligne_commande.materiel_id=spas_materiel.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                group by spas_commande.id,spas_commande.date_c,spas_commande.ref_c
                order by spas_commande.ref_c desc
            """

    lcoms = Commande.objects.raw(query, [active, en_cours])
    #lcoms = Ligne_commande.objects.order_by('-id')  par ordre décroissant
    paginator = Paginator(lcoms, 10)
    page = request.GET.get('page')
    try:
        lcoms = paginator.page(page)
    except PageNotAnInteger:
        lcoms = paginator.page(1)
    except EmptyPage:
        lcoms = paginator.page(paginator.num_pages)

    context = {'lcoms': lcoms,'paginator':paginator}
    return render(request, 'patrimoine/lmcommande/lmcommande.html', context)


# recherhe des materiels commandées
def search_materiel_commandee(request):

    if request.method == "GET" and 'date_mcmd' in request.GET:
        date_mcmd = request.GET.get('date_mcmd')
        if (date_mcmd != ''):
            mcmds = Ligne_commande.objects.filter(commande__date_c=date_mcmd, etat='ACTIVE')
            context = {'date_mcmd': date_mcmd, 'mcmds': mcmds}
            return render(request, 'patrimoine/lmcommande/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'patrimoine/lmcommande/search.html')


#Liste détaillé - materiel commandé
def detail_lmcommande(request, id):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_commande.id,spas_materiel.nom,spas_materiel.ref_mat,spas_ligne_commande.qte_c,
                spas_ligne_commande.prix_c,spas_commande.ref_c,spas_commande.date_c,spas_ligne_commande.obs_c
                from spas_ligne_commande,spas_commande,spas_materiel
                where spas_ligne_commande.materiel_id=spas_materiel.id
                and spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_commande.id=%s
            """

    lcoms = Ligne_commande.objects.raw(query, [active, en_cours, id])
    paginator = Paginator(lcoms, 10)
    page = request.GET.get('page')
    try:
        lcoms = paginator.page(page)
    except PageNotAnInteger:
        lcoms = paginator.page(1)
    except EmptyPage:
        lcoms = paginator.page(paginator.num_pages)

    context = {'lcoms': lcoms,'paginator':paginator}
    return render(request, 'patrimoine/lmcommande/lmcommande_detail.html', context)


#Création unique - materiel commandé
def create_lmcommande(request):
    form = Ligne_materiel_commandeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lmcommande')

    return render(request, 'patrimoine/lmcommande/lmcommande_form.html', {'form': form})


#Création multiple - materiel commandé
def create_mlcom(request):
    form = mLigne_comForm(request.POST or None)
    d = date.today().strftime("%d%m%Y")
    id_max = Commande.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_com = "CMD0" + str(id_max) + str(d)
    if request.method=='POST':
        date_com = request.POST['date_c']
        ref_com = request.POST['ref_c']
        mat = request.POST.getlist('fourIds[]')
        qte = request.POST.getlist('qtefour[]')
        obs = request.POST.getlist('obs_c[]')
        prix = request.POST.getlist('prices[]')
        if (mat):
            com = Commande.objects.create(ref_c=ref_com, date_c=date_com)
            commande_id = com.id
            for i in range(len(mat)):
                Ligne_commande.objects.create(commande=Commande.objects.get(pk=commande_id), materiel=Materiel.objects.get(pk=mat[i]), qte_c=qte[i], prix_c=prix[i], obs_c=obs[i])

            messages.success(request, "Enregistrement(s) effectué(s)")
            return redirect('list_lmcommande')
        else:
            messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne commande de fourniture.")
            return render(request, 'patrimoine/lmcommande/lmcom_form.html', {'form': form, 'ref': ref_com})

    return render(request, 'patrimoine/lmcommande/lmcom_form.html', {'form': form,'ref':ref_com})


#MAJ - materiel commandé
def update_lmcommande(request, id):
    com = get_object_or_404(Ligne_commande,id=id)
    form = Ligne_materiel_commandeForm(request.POST or None, instance=com)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_lmcommande')

    return render(request, 'patrimoine/lmcommande/lmcommande_form.html', {'form': form})


#Suppression - materiel commandé
def delete_lmcommande(request, id):
    lcom = get_object_or_404(Ligne_commande,id=id)

    if request.method == 'POST':
        lcom.etat = 'INACTIVE'
        lcom.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_lmcommande')

    return render(request, 'patrimoine/lmcommande/lmcommande_sup_confirm.html', {'lcom': lcom})

# Approvisionnement pour materiel (materiel_entree).

#Liste - materiel approvisionné
def list_lmentree(request):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_entree.id,spas_entree.date_e,spas_entree.ref_e,count(spas_ligne_entree.materiel_id) as nbmat,
                sum(spas_ligne_entree.qte_e) as qte_total,sum(spas_ligne_entree.prix_e) as prix_total
                from spas_ligne_entree,spas_entree,spas_materiel
                where spas_ligne_entree.materiel_id=spas_materiel.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
                group by spas_entree.id,spas_entree.date_e,spas_entree.ref_e
                order by spas_entree.ref_e desc
            """

    lments = Entree.objects.raw(query, [active, en_cours])
    #lments = Ligne_entree.objects.filter(etat='ACTIVE', materiel__isnull=False).order_by('-id') # par ordre décroissant
    paginator = Paginator(lments, 10)
    page = request.GET.get('page')
    try:
        lments = paginator.page(page)
    except PageNotAnInteger:
        lments = paginator.page(1)
    except EmptyPage:
        lments = paginator.page(paginator.num_pages)

    context = {'lments': lments,'paginator':paginator}
    return render(request, 'patrimoine/lmentree/lentree.html', context)


# recherhe des materiels entrées
def search_materiel_entree(request):

    if request.method == "GET" and 'date_ment' in request.GET:
        date_ment = request.GET.get('date_ment')
        if (date_ment != ''):
            ments = Ligne_entree.objects.filter(entree__date_e=date_ment, etat='ACTIVE')
            context = {'date_ment': date_ment, 'ments': ments}
            return render(request, 'patrimoine/lmentree/search.html', context)
        else:
            messages.warning(request, "Veuillez saisir une donnée correcte :-)")

    return render(request, 'patrimoine/lmentree/search.html')


#Liste détaillé - materiel approvisionné
def detail_list_lmentree(request, id):
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select spas_ligne_entree.id,spas_materiel.nom,spas_fournisseur.nom as nomf,spas_ligne_entree.qte_e,
                spas_ligne_entree.prix_e,spas_entree.ref_e,spas_entree.date_e
                from spas_ligne_entree,spas_materiel,spas_entree,spas_fournisseur
                where spas_ligne_entree.materiel_id=spas_materiel.id
                and spas_ligne_entree.entree_id=spas_entree.id
                and spas_entree.fournisseur_id=spas_fournisseur.id
                and spas_ligne_entree.etat=%s
                and spas_ligne_entree.statut=%s
                and spas_ligne_entree.entree_id=%s
            """

    lments = Ligne_entree.objects.raw(query, [active, en_cours, id])
    paginator = Paginator(lments, 10)
    page = request.GET.get('page')
    try:
        lments = paginator.page(page)
    except PageNotAnInteger:
        lments = paginator.page(1)
    except EmptyPage:
        lments = paginator.page(paginator.num_pages)

    context = {'lments': lments, 'paginator': paginator}
    return render(request, 'patrimoine/lmentree/lentree_detail.html', context)


#Création unique - materiel approvisionné
def create_lmentree(request):
    form = Ligne_entreemForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_lmentree')

    return render(request, 'patrimoine/lmentree/lentree_form.html', {'form': form})


#Chargement de la liste déroulante des materiels commandés sur la page des materiel approvisionné
def load_materiel_cmd(request):
    cmd_ref = request.GET.get('cmd_ref')
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
               select spas_ligne_commande.id, spas_ligne_commande.materiel_id,spas_materiel.ref_mat,spas_materiel.nom
               from spas_ligne_commande,spas_commande,spas_materiel
               where spas_ligne_commande.commande_id=spas_commande.id
               and spas_ligne_commande.materiel_id=spas_materiel.id
               and spas_ligne_commande.etat=%s
               and spas_ligne_commande.statut=%s
               and spas_commande.ref_c=%s
            """

    m_cmds = Ligne_commande.objects.raw(query, [active, en_cours, cmd_ref])
    return render(request, 'patrimoine/lentree/materiel_cmd.html', {'m_cmds': m_cmds})


#Création multiple - materiel approvisionné
def create_mlent(request):
    form = mLentreForm(request.POST or None)
    active = 'ACTIVE'
    en_cours = 'EN COURS'
    query = """
                select distinct spas_commande.id,spas_commande.ref_c
                from spas_ligne_commande,spas_commande
                where spas_ligne_commande.commande_id=spas_commande.id
                and spas_ligne_commande.etat=%s
                and spas_ligne_commande.statut=%s
                and spas_ligne_commande.materiel_id is not null 
                order by spas_commande.ref_c desc
            """

    commande = Commande.objects.raw(query, [active, en_cours])
    d = date.today().strftime("%d%m%Y")
    id_max = Entree.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_ent = "APPRO" + str(id_max) + str(d)
    if request.method=='POST':
        date_e = request.POST['date_e']
        ref_e = request.POST['ref_e']
        fournis = request.POST['fournisseur']
        employe = request.user.id
        mat = request.POST.getlist('fourIds[]') #mat represente la ligne commande ou il y a le materiel cmdé
        materiel_id = request.POST.getlist('MatId[]') #materiel_id represente l'id du materiel en question
        qte = request.POST.getlist('qtefour[]')
        prix = request.POST.getlist('prices[]')
        if (date_e and ref_e and fournis and employe):
            if (mat and materiel_id):
                ent = Entree.objects.create(ref_e=ref_e, date_e=date_e, fournisseur=Fournisseur.objects.get(pk=fournis),employe=MyUser.objects.get(pk=employe))
                entree_id = ent.id
                for i in range(len(mat)):
                    mat_entree = Ligne_entree.objects.create(entree=Entree.objects.get(pk=entree_id), commande=Ligne_commande.objects.get(pk=mat[i]), materiel=Materiel.objects.get(pk=materiel_id[i]), qte_e=qte[i], prix_e=prix[i])
                    mat_entree_id = mat_entree.id
                    Mouvement.objects.create(date_m=date_e, ligne_appro=Ligne_entree.objects.get(pk=mat_entree_id), materiel=Materiel.objects.get(pk=materiel_id[i]), qte=qte[i], type='APPRO')
                    Ligne_commande.objects.filter(id=mat[i]).update(statut='LIVREE')

                messages.success(request, "Enregistrement(s) effectué(s)")
                return redirect('list_lmentree')
            else:
                messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne de matériel.")
                return render(request, 'patrimoine/lmentree/mlentre_form.html', {'form': form, 'ref': ref_ent, 'commande':commande})
        else:
            messages.warning(request, "Svp, Veuillez remplir toutes les zones de saisies.")
            return render(request, 'patrimoine/lmentree/mlentre_form.html', {'form': form, 'ref': ref_ent, 'commande':commande})

    return render(request, 'patrimoine/lmentree/mlentre_form.html', {'form': form,'ref':ref_ent, 'commande':commande})


#Chargement automatique de l'id du materiel sur la page entree(appro)
def load_materiel(request):
    com_id = request.GET.get('ligne_commande')
    mat_id = get_object_or_404(Ligne_commande,id=com_id)
    mId = mat_id.materiel.id
    return JsonResponse(mId, safe=False)


#MAJ - materiel approvisionné
def update_lmentree(request, id):
    ent = get_object_or_404(Ligne_entree,id=id)
    mouv = get_object_or_404(Mouvement,ligne_appro_id=ent)
    form = Ligne_entreemForm(request.POST or None, instance=ent)

    #verification si la livraison est déja utilisé(présent dans la table sortie)
    ent_utilise = list(Affectation.objects.filter(materiel_id=ent.materiel_id, etat='ACTIVE').aggregate(Sum('materiel_id')).values())[0] or 0

    if form.is_valid():
        if ent_utilise == 0:
            postm = form.save(commit=False)
            # Mise a jour automatique des donnees de la table mouvement
            details = get_object_or_404(Entree,ref_e=postm.entree)
            date_entree = details.date_e
            mouv.date_m = date_entree
            mouv.materiel = postm.materiel
            mouv.qte = postm.qte_e
            # Fin de la Mise a jour automatique des donnees de la table mouvement
            postm.save()
            mouv.save()
            messages.success(request, "Modification effectuée")
            return redirect('list_lmentree')
        else:
            messages.success(request, "Modification impossible, le matériel est deja affecte.")
            return redirect('list_lmentree')

    return render(request, 'lmentree/lentree_form.html', {'form': form, 'ent': ent})


#Suppression - materiel approvisionné
def delete_lmentree(request, id):
    lent = get_object_or_404(Ligne_entree,id=id)
    mouv = get_object_or_404(Mouvement,ligne_appro_id=lent)

    #verification si la livraison est déja utilisé(présent dans la table sortie)
    lent_utilise = list(Affectation.objects.filter(materiel_id=lent.materiel_id, etat='ACTIVE').aggregate(Sum('materiel_id')).values())[0] or 0

    if request.method == 'POST':
        if lent_utilise == 0:
            # permet d'actualiser la ligne commande ou le consommable est en cours au cas ou il serait préalablement livrée dans
            # la table ligne commande
            commande_id = lent.commande_id
            Ligne_commande.objects.filter(id=commande_id).update(statut='EN COURS')
            lent.etat = 'INACTIVE'
            mouv.etat = 'INACTIVE'
            lent.save()
            mouv.save()
            messages.success(request, "Suppression effectuée")
            return redirect('list_lmentree')
        else:
            messages.success(request, "Suppression impossible, le materiel est deja affecte.")
            return redirect('list_lmentree')

    return render(request, 'patrimoine/lmentree/lentree_sup_confirm.html', {'lent': lent})


# etats sur patrimoine
def search_maintenance_mois(request):
    active = 'ACTIVE'
    query = """ select spas_maintenance.id,spas_materiel.ref_mat,spas_materiel.nom,spas_maintenance.type_m,spas_maintenance.date_d,
                spas_maintenance.date_f
                from spas_maintenance,spas_materiel
                where spas_maintenance.materiel_id=spas_materiel.id
                and EXTRACT(MONTH FROM spas_maintenance.date_d) = EXTRACT(MONTH FROM now())
                and spas_maintenance.etat = %s
            """
    maint_cours = Maintenance.objects.raw(query, [active])
    context = {'maint_cours': maint_cours}
    return render(request, 'etat/patrimoine/maintenance_preventive.html', context)


# etats sur patrimoine - pdf
class Maintenance_cours(View):
    def get(self, request, *args, **kwargs):
        active = 'ACTIVE'

        query = """ select spas_maintenance.id,spas_materiel.ref_mat,spas_materiel.nom,spas_maintenance.type_m,spas_maintenance.date_d,
                    spas_maintenance.date_f
                    from spas_maintenance,spas_materiel
                    where spas_maintenance.materiel_id=spas_materiel.id
                    and EXTRACT(MONTH FROM spas_maintenance.date_d) = EXTRACT(MONTH FROM now())
                    and spas_maintenance.etat = %s
                """
        maint_cours = Maintenance.objects.raw(query, [active])
        data = {
            'today': datetime.date.today(),
            'mats': maint_cours,
        }
        pdf = render_to_pdf('etat/patrimoine/maintenance_mois.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


### Configurations

# Configuration de la page d'erreur
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

#Liste - service
@login_required
def list_u_orga(request):
    u_orgas = Unite_organisation.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(u_orgas, 10)
    page = request.GET.get('page')
    try:
        u_orgas = paginator.page(page)
    except PageNotAnInteger:
        u_orgas = paginator.page(1)
    except EmptyPage:
        u_orgas = paginator.page(paginator.num_pages)

    context = {'u_orgas': u_orgas,'paginator':paginator}
    return render(request, 'configuration/u_orga/u_orga.html', context)


#Création - service
def create_u_orga(request):
    form = U_orgaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_u_orga')

    return render(request, 'configuration/u_orga/u_orga_form.html', {'form': form})


#MAJ - service
def update_u_orga(request, id):
    u_orga = get_object_or_404(Unite_organisation,id=id)
    form = U_orgaForm(request.POST or None, instance=u_orga)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_u_orga')

    return render(request, 'configuration/u_orga/u_orga_form.html', {'form': form})


#Suppression - service
def delete_u_orga(request, id):
    u_orga = get_object_or_404(Unite_organisation,id=id)

    if request.method == 'POST':
        u_orga.etat = 'INACTIVE'
        u_orga.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_u_orga')

    return render(request, 'configuration/u_orga/u_orga_sup_confirm.html', {'u_orga': u_orga})


#Liste - employe
@login_required
def list_employe(request):
    employes = Employe.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(employes, 10)
    page = request.GET.get('page')
    try:
        employes = paginator.page(page)
    except PageNotAnInteger:
        employes = paginator.page(1)
    except EmptyPage:
        employes = paginator.page(paginator.num_pages)

    context = {'employes': employes,'paginator':paginator}
    return render(request, 'configuration/employe/employe.html', context)


#Création - employe
def create_employe(request):
    form = EmployeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_employe')

    return render(request, 'configuration/employe/employe_form.html', {'form': form})


#MAJ - employe
def update_employe(request, id):
    employe = get_object_or_404(Employe,id=id)
    form = EmployeForm(request.POST or None, instance=employe)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_employe')

    return render(request, 'configuration/employe/employe_form.html', {'form': form})


#Suppression - employe
def delete_employe(request, id):
    employe = get_object_or_404(Employe,id=id)

    if request.method == 'POST':
        employe.etat = 'INACTIVE'
        employe.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_employe')

    return render(request, 'configuration/employe/employe_sup_confirm.html', {'employe': employe})


#Liste - employe - service (employe_service)
@login_required
def list_employe_unite(request):
    employe_us = Employe_service.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(employe_us, 10)
    page = request.GET.get('page')

    try:
        employe_us = paginator.page(page)
    except PageNotAnInteger:
        employe_us = paginator.page(1)
    except EmptyPage:
        employe_us = paginator.page(paginator.num_pages)

    context = {'employe_us': employe_us,'paginator':paginator}
    return render(request, 'configuration/employe_unite/employe_unite.html', context)


#Création - employe - service
def create_employe_unite(request):
    form = Employe_UniteForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_employe_unite')

    return render(request, 'configuration/employe_unite/employe_unite_form.html', {'form': form})


#MAJ - employe - service
def update_employe_unite(request, id):
    employe_u = get_object_or_404(Employe_service,id=id)
    form = Employe_UniteForm(request.POST or None, instance=employe_u)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_employe_unite')

    return render(request, 'configuration/employe_unite/employe_unite_form.html', {'form': form})


#Suppression - employe - service 
def delete_employe_unite(request, id):
    employe_u = get_object_or_404(Employe_service,id=id)

    if request.method == 'POST':
        employe_u.etat = 'INACTIVE'
        employe_u.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_employe_unite')

    return render(request, 'configuration/employe_unite/employe_unite_sup_confirm.html', {'employe_u': employe_u})


#Liste - fournisseur
@login_required
def list_fournisseur(request):
    fours = Fournisseur.objects.filter(etat='ACTIVE').order_by('-id') # par ordre décroissant
    paginator = Paginator(fours, 10)
    page = request.GET.get('page')
    try:
        fours = paginator.page(page)
    except PageNotAnInteger:
        fours = paginator.page(1)
    except EmptyPage:
        fours = paginator.page(paginator.num_pages)

    context = {'fours': fours,'paginator':paginator}
    return render(request, 'configuration/fournisseur/fournisseur.html', context)


#Création - fournisseur
def create_fournisseur(request):
    form = FournisseurForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_fournisseur')

    return render(request, 'configuration/fournisseur/fournisseur_form.html', {'form': form})


#MAJ - fournisseur
def update_fournisseur(request, id):
    four = get_object_or_404(Fournisseur,id=id)
    form = FournisseurForm(request.POST or None, instance=four)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_fournisseur')

    return render(request, 'configuration/fournisseur/fournisseur_form.html', {'form': form})


#Suppression - fournisseur
def delete_fournisseur(request, id):
    four = get_object_or_404(Fournisseur,id=id)

    if request.method == 'POST':
        four.etat = 'INACTIVE'
        four.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_fournisseur')

    return render(request, 'configuration/fournisseur/fournisseur_sup_confirm.html', {'four': four})


#Liste - seuil.
@login_required
def list_seuil(request):
    seus = Seuil.objects.order_by('id') # par ordre décroissant
    paginator = Paginator(seus, 10)
    page = request.GET.get('page')
    try:
        seus = paginator.page(page)
    except PageNotAnInteger:
        seus = paginator.page(1)
    except EmptyPage:
        seus = paginator.page(paginator.num_pages)

    context = {'seus': seus,'paginator':paginator}
    return render(request, 'configuration/seuil/seuil.html', context)


#Création - seuil
def create_seuil(request):
    form = SeuilForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Enregistrement effectué")
        return redirect('list_seuil')

    return render(request, 'configuration/seuil/seuil_form.html', {'form': form})


#MAJ - seuil
def update_seuil(request, id):
    seus = get_object_or_404(Seuil,id=id)
    form = SeuilForm(request.POST or None, instance=seus)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée")
        return redirect('list_seuil')

    return render(request, 'configuration/seuil/seuil_form.html', {'form': form})


#Suppression - seuil
def delete_seuil(request, id):
    seus = get_object_or_404(Seuil,id=id)

    if request.method == 'POST':
        seus.etat = 'INACTIVE'
        seus.save()
        messages.success(request, "Suppression effectuée")
        return redirect('list_seuil')

    return render(request, 'configuration/seuil/seuil_sup_confirm.html', {'seus': seus})