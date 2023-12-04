from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Filme, Episodio, User

# Só existe para aparecer o campo personalizado filmes_visto
field = list(UserAdmin.fieldsets)
field.append(
    ("Histórico", {'fields': ('filmes_vistos',)})
)
UserAdmin.fieldsets = tuple(field)
 

# Register your models here.
admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(User, UserAdmin)
