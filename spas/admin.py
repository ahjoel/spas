from django.contrib import admin
from spas.models import MyUser,Employe,Unite_organisation,Mouvement
# Register your models here.

admin.site.site_header = 'SPAS'

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','u_orga')

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'pseudo', 'email','employe')

class Unite_organisationAdmin(admin.ModelAdmin):
    list_display = ('nom_uo',)

class MouvementAdmin(admin.ModelAdmin):
    list_display = ('date_m','fourniture','consommable','materiel','qte','type')

admin.site.register(Employe, EmployeAdmin)
admin.site.register(Unite_organisation, Unite_organisationAdmin)
admin.site.register(Mouvement, MouvementAdmin)
admin.site.register(MyUser, MyUserAdmin)
