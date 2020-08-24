from django.contrib import admin
import core.comunicacao.e_mail.models
# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ['nm_descritivo', 'endereco']


admin.site.register(core.comunicacao.e_mail.models.EmailEndereco)

admin.site.register(core.comunicacao.e_mail.models.Email)