from django.contrib import admin

from .models import Invitado


@admin.register(Invitado)
class InvitadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'evento')
    list_filter = ('evento',)
    search_fields = ('nombre', 'cedula')
