from django.contrib import admin
import core.filial.models
# Register your models here.


class FilialAdmin(admin.ModelAdmin):
    ordering = ['cd_filial']
    list_display = ['cd_filial', 'nome']


class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']


class FilialServicoAdmin(admin.ModelAdmin):
    list_display = ['cd_filial', 'servico']


class FilialHoraFuncionamentoAdmin(admin.ModelAdmin):
    list_display = ['cd_filial', 'cd_hr_util_inicio', 'cd_hr_util_fim', 'cd_hr_sab_inicio',
                    'cd_hr_sab_fim', 'cd_hr_dom_inicio', 'cd_hr_dom_fim']


admin.site.register(core.filial.models.Filial, FilialAdmin)
admin.site.register(core.filial.models.Servico, ServicoAdmin)
admin.site.register(core.filial.models.FilialServico, FilialServicoAdmin)
admin.site.register(core.filial.models.FilialHoraFuncionamento, FilialHoraFuncionamentoAdmin)
