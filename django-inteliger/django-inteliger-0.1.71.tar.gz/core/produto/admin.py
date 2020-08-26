from django.contrib import admin
import core.produto.models
# Register your models here.


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['cd_produto', 'nome', 'nm_ecommerce', 'nm_url_ecommerce', 'is_ecommerce']
    ordering = ['cd_produto']


class PrecoListaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'dat_ini', 'dat_fim']


class ProdutoPrecoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'precolista']


admin.site.register(core.produto.models.Produto, ProdutoAdmin)
admin.site.register(core.produto.models.ProdutoImagem)
admin.site.register(core.produto.models.Marca)
admin.site.register(core.produto.models.Categoria)

admin.site.register(core.produto.models.PrecoLista, PrecoListaAdmin)
admin.site.register(core.produto.models.ProdutoPreco, ProdutoPrecoAdmin)