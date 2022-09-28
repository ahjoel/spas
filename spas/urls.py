from django.urls import path
from django.contrib.auth import logout

from . import views

urlpatterns = [
    # route pour la page d'acceuil
    path('', views.index, name='home'),
    path('testt', views.indext, name='testt'),
    path('log', views.loginPage, name='log'),

    ## Gestion du stock

    # routes pour les types
    path('type/', views.list_type, name='list_type'),
    path('ctype/', views.create_type, name='create_type'),
    path('utype/<int:id>', views.update_type, name='update_type'),
    path('dtype/<int:id>', views.delete_type, name='delete_type'),

    # routes pour les fournitures
    path('fourniture/', views.list_fourniture, name='list_fourniture'),
    path('cfourniture/', views.create_fourniture, name='create_fourniture'),
    path('sfourniture', views.search_fourniture, name='search_fourniture'),
    path('ufourniture/<int:id>', views.update_fourniture, name='update_fourniture'),
    path('dfourniture/<int:id>', views.delete_fourniture, name='delete_fourniture'),

    # routes pour les ligne_commandes (fourniture commandés)
    path('lcommande/', views.list_lcommande, name='list_lcommande'),
    path('detlcommande/<int:id>', views.detail_lcommande, name='detail_lcommande'),
    path('clcommande', views.create_lcommande, name='create_lcommande'),
    path('cflcommande', views.create_flcom, name='create_flcom'),
    path('slcommande', views.search_fourniture_commandee, name='search_fourniture_cmd'),
    path('ulcommande/<int:id>', views.update_lcommande, name='update_lcommande'),
    path('dlcommande/<int:id>', views.delete_lcommande, name='delete_lcommande'),

    # routes pour les ligne_entrees (fourniture entree)
    path('lentree/', views.list_lentree, name='list_lentree'),
    path('detlentree/<int:id>', views.detail_list_lentree, name='detail_lentree'),
    path('cflentree', views.create_flent, name='create_lentree'),
    path('slentree', views.search_fourniture_entree, name='search_fourniture_entree'),
    path('ulentree/<int:id>', views.update_lentree, name='update_lentree'),
    path('dlentree/<int:id>', views.delete_lentree, name='delete_lentree'),

    #route pour le chargement de l'id de la fourniture sur la page achat pour fourniture
    path('ajax/load_four/', views.load_fourniture, name='ajax_load_four'),

    # routes pour les ligne_sorties (fourniture sortie)
    path('lsortie/', views.list_lsortie, name='list_lsortie'),
    path('detlsortie/<int:id>', views.detail_list_lsortie, name='detail_lsortie'),
    path('cflsortie/', views.create_flsor, name='create_lsortie'),
    path('slsortie/', views.search_fourniture_sortie, name='search_fourniture_sortie'),
    path('ulsortie/<int:id>', views.update_lsortie, name='update_lsortie'),
    path('dlsortie/<int:id>', views.delete_lsortie, name='delete_lsortie'),
    path('lmouvappsortie', views.list_mouv_appro_sortie, name='list_mouvapprosortie'),

    #route pour le chargement de la quantité disponibles des fournitures
    path('ajax/load_qte/', views.load_qte_fourniture, name='ajax_load_qte'),

    #route pour le chargement des commande de fournitures
    path('ajax/load_cmd/', views.load_fourniture_cmd, name='ajax_load_cmd'),

    #route pour les etats - situation periode des fournitures
    path('lsit_p', views.search_stock_periode, name='sit_period'),

    #route pour les etats - situation periode des fournitures - export pdf
    path('pdf_view/', views.ViewPDF.as_view(), name='pdf_view'),

    #path('pdf_download/', ligne_sortie.downloadPDF.as_view(), name='pdf_download'),
    path('cmd_c', views.search_stock_cmd_cours, name='cmd_c'),

    #route pour les etats - commande en cours pour les fournitures - export pdf
    path('pdf_view_cmdc/', views.Commande_cours.as_view(), name='commande_en_cours'),

    #path('pdf_download/', ligne_sortie.downloadPDF.as_view(), name='pdf_download'),
    
    ## Partie Consommable
    
    # routes pour les consommables
    path('consommable/', views.list_consommable, name='list_consommable'),
    path('cconsommable/', views.create_consommable, name='create_consommable'),
    path('uconsommable/<int:id>', views.update_consommable, name='update_consommable'),
    path('dconsommable/<int:id>', views.delete_consommable, name='delete_consommable'),

    # routes pour les ligne_commandes (consommable commandés)
    path('lccommande/', views.list_lccommande, name='list_lccommande'),
    path('detlccommande/<int:id>', views.detail_lccommande, name='detail_lccommande'),
    path('clccommande/', views.create_lccommande, name='create_lccommande'),
    path('cclcommande/', views.create_clcom, name='create_clcom'),
    path('slccommande/', views.search_consommable_commande, name='search_consommable_cmd'),
    path('ulccommande/<int:id>', views.update_lccommande, name='update_lccommande'),
    path('dlccommande/<int:id>', views.delete_lccommande, name='delete_lccommande'),

    # routes pour les ligne_entrees (consommable entree)
    path('lcentree/', views.list_lcentree, name='list_lcentree'),
    path('detlcentree/<int:id>', views.detail_list_lcentree, name='detail_lcentree'),
    path('cclentree/', views.create_clent, name='create_lcentree'),
    path('slcentree/', views.search_consommable_entree, name='search_consommable_entree'),
    path('ulcentree/<int:id>', views.update_lcentree, name='update_lcentree'),
    path('dlcentree/<int:id>', views.delete_lcentree, name='delete_lcentree'),
    path('lmouvcappsortie/', views.list_mouv_con_appro_sortie, name='list_mouvcapprosortie'),

    #route pour le chargement de l'id du consommable sur la page achat pour consommable
    path('ajax/load_con/', views.load_consommable, name='ajax_load_con'),

    # routes pour les ligne_sorties (consommable sortie)
    path('lcsortie/', views.list_lcsortie, name='list_lcsortie'),
    path('detlcsortie/<int:id>', views.detail_list_lcsortie, name='detail_lcsortie'),
    path('clcsortie/', views.create_clsor, name='create_clsor'),
    path('slcsortie/', views.search_consommable_sortie, name='search_consommable_sortie'),
    path('ulcsortie/<int:id>', views.update_lcsortie, name='update_lcsortie'),
    path('dlcsortie/<int:id>', views.delete_lcsortie, name='delete_lcsortie'),

    #route pour le chargement de la quantité disponibles de consommable
    path('ajax/load_qtec/', views.load_qte_consommable, name='ajax_load_qtec'),

    # route pour le chargement des commande de consommable
    path('ajax/load_cmd_c/', views.load_consommable_cmd, name='ajax_load_cmd_c'),


    ## Gestion du patrimoine

    # routes pour les modeles
    path('modele/', views.list_modele, name='list_modele'),
    path('cmodele/', views.create_modele, name='create_modele'),
    path('umodele/<int:id>', views.update_modele, name='update_modele'),
    path('dmodele/<int:id>', views.delete_modele, name='delete_modele'),

    # routes pour les matériels
    path('materiel/', views.list_materiel, name='list_materiel'),
    path('cmateriel/', views.create_materiel, name='create_materiel'),
    path('smateriel/', views.search_materiel, name='search_materiel'),
    path('umateriel/<int:id>', views.update_materiel, name='update_materiel'),
    path('dmateriel/<int:id>', views.delete_materiel, name='delete_materiel'),

    # routes pour les maintenances
    path('maintenance/', views.list_maintenance, name='list_maintenance'),
    path('cmaintenance/', views.create_maintenance, name='create_maintenance'),
    path('umaintenance/<int:id>', views.update_maintenance, name='update_maintenance'),
    path('dmaintenance/<int:id>', views.delete_maintenance, name='delete_maintenance'),

    # routes pour les ligne_commandes (materiel commandés)
    path('lmcommande/', views.list_lmcommande, name='list_lmcommande'),
    path('detlmcommande/<int:id>', views.detail_lmcommande, name='detail_lmcommande'),
    path('clmcommande/', views.create_lmcommande, name='create_lmcommande'),
    path('cmlcommande/', views.create_mlcom, name='create_mlcom'),
    path('slmcommande/', views.search_materiel_commandee, name='search_materiel_cmd'),
    path('ulmcommande/<int:id>', views.update_lmcommande, name='update_lmcommande'),
    path('dlmcommande/<int:id>', views.delete_lmcommande, name='delete_lmcommande'),
    
    # routes pour les ligne_entrees (matériel entree)
    path('lmentree/', views.list_lmentree, name='list_lmentree'),
    path('detlmentree/<int:id>', views.detail_list_lmentree, name='detail_lmentree'),
    path('cmlentree/', views.create_mlent, name='create_lmentree'),
    path('slmentree/', views.search_materiel_entree, name='search_materiel_entree'),
    path('ulmentree/<int:id>', views.update_lmentree, name='update_lmentree'),
    path('dlmentree/<int:id>', views.delete_lmentree, name='delete_lmentree'),

    #route pour le chargement de l'id du materiel sur la page achat pour materiel
    path('ajax/load_mat/', views.load_materiel, name='ajax_load_mat'),

    # routes pour les affectations de matériel (sortie de materiel)
    path('affectation/', views.list_affectation, name='list_affectation'),
    path('caffectation/', views.create_affectation, name='create_affectation'),
    path('saffectation/', views.search_materiel_affecte, name='search_materiel_affect'),
    path('uaffectation/<int:id>', views.update_affectation, name='update_affectation'),
    path('daffectation/<int:id>', views.delete_affectation, name='delete_affectation'),

    #route pour le chargement des commande de materiel
    path('ajax/load_cmd_m/', views.load_materiel_cmd, name='ajax_load_cmd_m'),
    path('maint_c/', views.search_maintenance_mois, name='maint_c'),

    #route pour les etats - commande en cours pour les fournitures - export pdf
    path('pdf_view_maintc/', views.Maintenance_cours.as_view(), name='maitenance_en_cours'),


    ## Gestion des configurations

    # routes pour les unites_organisation
    path('u_orga/', views.list_u_orga, name='list_u_orga'),
    path('cu_orga/', views.create_u_orga, name='create_u_orga'),
    path('uu_orga/<int:id>', views.update_u_orga, name='update_u_orga'),
    path('du_orga/<int:id>', views.delete_u_orga, name='delete_u_orga'),

    # routes pour les employés
    path('employe/', views.list_employe, name='list_employe'),
    path('cemploye/', views.create_employe, name='create_employe'),
    path('uemploye/<int:id>', views.update_employe, name='update_employe'),
    path('demploye/<int:id>', views.delete_employe, name='delete_employe'),

    # routes pour les employés - unite
    path('employe_u/', views.list_employe_unite, name='list_employe_unite'),
    path('cemploye_u/', views.create_employe_unite, name='create_employe_unite'),
    path('uemploye_u/<int:id>', views.update_employe_unite, name='update_employe_unite'),
    path('demploye_u/<int:id>', views.delete_employe_unite, name='delete_employe_unite'),

    # routes pour les fournisseurs
    path('fournisseur/', views.list_fournisseur, name='list_fournisseur'),
    path('cfournisseur/', views.create_fournisseur, name='create_fournisseur'),
    path('ufournisseur/<int:id>', views.update_fournisseur, name='update_fournisseur'),
    path('dfournisseur/<int:id>', views.delete_fournisseur, name='delete_fournisseur'),

    #route pour le chargement des utilisateurs
    path('ajax/load_serv/', views.load_service_utilisateur, name='ajax_load_serv'),
 
    # routes pour les seuils de fournitures
    path('seuil/', views.list_seuil, name='list_seuil'),
    path('cseuil/', views.create_seuil, name='create_seuil'),
    path('useuil/<int:id>', views.update_seuil, name='update_seuil'),
    path('dseuil/<int:id>', views.delete_seuil, name='delete_seuil'),
]

handler404 = "spas.views.page_not_found_view"