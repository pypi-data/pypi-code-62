from django.db import models
import core.models


# Create your models here.
class Produto(core.models.Log):
    """
    :Nome da classe/função: Produto
    :descrição: Classe de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    cd_produto = models.IntegerField(primary_key=True)
    cd_externo = models.IntegerField(null=True, blank=True)

    nome = models.CharField(max_length=200, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    marca = models.ForeignKey('produto.Marca', on_delete=models.DO_NOTHING, related_name='marca', null=True, blank=True)
    tipo_produto = models.ForeignKey('produto.Tipo', on_delete=models.DO_NOTHING, null=True, blank=True)
    fabricante = models.ForeignKey('fornecedor.Fabricante', on_delete=models.DO_NOTHING, null=True, blank=True)

    imagem = models.FileField(upload_to="produtos", default='produtos/caixa-nissei.jpg', null=True, blank=True)

    produto_pai = models.ForeignKey('self', models.DO_NOTHING, null=True, blank=True)

    is_ecommerce = models.BooleanField(default=True, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=200, null=True, blank=True)
    nm_ecommerce = models.CharField(max_length=200, null=True, blank=True)
    descricao_ecommerce = models.TextField(null=True, blank=True)
    altura_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    largura_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    profundidade_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    peso_ecommerce = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    qtd_min_venda_ecommerce = models.IntegerField(null=True, blank=True, default=1)
    qtd_max_venda_ecommerce = models.IntegerField(null=True, blank=True)

    is_retencao_receita = models.BooleanField(default=False, null=True, blank=True)
    is_venda_controlada = models.BooleanField(default=False, null=True, blank=True)
    is_pbm = models.BooleanField(default=False, null=True, blank=True)

    categoria_principal = models.ForeignKey('produto.Categoria', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='categoria_principal')

    grupo = models.ManyToManyField('produto.Grupo', through='produto.ProdutoGrupo', through_fields=('produto', 'grupo'))
    categoria = models.ManyToManyField('produto.Categoria', through='produto.ProdutoCategoria', through_fields=('produto', 'categoria'))
    kit = models.ManyToManyField('produto.Kit', through='produto.ProdutoKit', through_fields=('produto', 'kit'))
    bula = models.ManyToManyField('produto.Bula', through='produto.ProdutoBula', through_fields=('produto', 'bula'))
    tipo_receita = models.ManyToManyField('produto.TipoReceita', through='produto.ProdutoTipoReceita', through_fields=('produto', 'tipo_receita'))
    principio_ativo = models.ManyToManyField('produto.PrincipioAtivo', through='produto.ProdutoPrincipioAtivo', through_fields=('produto', 'principio_ativo'))
    especialidade = models.ManyToManyField('produto.Especialidade', through='produto.ProdutoEspecialidade', through_fields=('produto', 'especialidade'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto'

    def __str__(self):
        return self.nome


class Tipo(core.models.Log):
    """
    :Nome da classe/função: Tipo
    :descrição: Classe de tipos de produtos possíveis
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tipo'


class Marca(core.models.Log):
    """
    :Nome da classe/função: Marca
    :descrição: Classe de marcas de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    descricao = models.CharField(max_length=500, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True, blank=True)
    nm_ecommerce = models.CharField(max_length=200, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_marca'

    def __str__(self):
        return self.nome


class ProdutoImagem(core.models.Log):
    """
    :Nome da classe/função: ProdutoImagem
    :descrição: Classe de relação entre imagens e produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    imagem = models.FileField(upload_to="produtos", default='produtos/caixa-nissei.jpg', null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_imagem'


class Grupo(core.models.Log):
    """
    :Nome da classe/função: Grupo
    :descrição: Classe de grupos de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    descricao = models.CharField(max_length=500, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_grupo'


class ProdutoGrupo(core.models.Log):
    """
    :Nome da classe/função: ProdutoGrupo
    :descrição: Classe de relação entre produtos e grupos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    grupo = models.ForeignKey('produto.Grupo', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtogrupo'


class Categoria(core.models.Log):
    """
    :Nome da classe/função: Categoria
    :descrição: Classe de categorias de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    categoria_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_categoria'


class ProdutoCategoria(core.models.Log):
    """
    :Nome da classe/função: ProdutoCategoria
    :descrição: Classe de relação entre produtos e categorias
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    categoria = models.ForeignKey('produto.Categoria', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtocategoria'


class Kit(core.models.Log):
    """
    :Nome da classe/função: Kit
    :descrição: Classe de kits de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_kit'


class ProdutoKit(core.models.Log):
    """
    :Nome da classe/função: ProdutoKit
    :descrição: Classe de relação entre produtos e kits
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    kit = models.ForeignKey('produto.Kit', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtokit'


class Bula(core.models.Log):
    """
    :Nome da classe/função: Bula
    :descrição: Classe de bulas de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_bula'


class ProdutoBula(core.models.Log):
    """
    :Nome da classe/função: ProdutoBula
    :descrição: Classe de relação entre produtos e bulas
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    bula = models.ForeignKey('produto.Bula', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtobula'


class TipoReceita(core.models.Log):
    """
    :Nome da classe/função: TipoReceita
    :descrição: Classe de tipos de receitas
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tiporeceita'


class ProdutoTipoReceita(core.models.Log):
    """
    :Nome da classe/função: ProdutoBula
    :descrição: Classe de relação entre produtos e tipos de receitas
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    tipo_receita = models.ForeignKey('produto.TipoReceita', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtotiporeceita'


class PrincipioAtivo(core.models.Log):
    """
    :Nome da classe/função: PrincipioAtivo
    :descrição: Classe de principios ativos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_principioativo'


class ProdutoPrincipioAtivo(core.models.Log):
    """
    :Nome da classe/função: ProdutoBula
    :descrição: Classe de relação entre produtos e principio ativos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    principio_ativo = models.ForeignKey('produto.PrincipioAtivo', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtoprincipioativo'


class Especialidade(core.models.Log):
    """
    :Nome da classe/função: Especialidade
    :descrição: Classe de especialidade de produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    nm_url_ecommerce = models.SlugField(max_length=100, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_especialidade'


class ProdutoEspecialidade(core.models.Log):
    """
    :Nome da classe/função: ProdutoEspecialidade
    :descrição: Classe de relação entre produtos e especialidades
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    especialidade = models.ForeignKey('produto.Especialidade', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtoespecialidade'


class ProdutoEan(core.models.Log):
    """
    :Nome da classe/função: ProdutoEan
    :descrição: Classe de relação entre produtos e EANs
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    ean = models.CharField(max_length=50, primary_key=True)
    is_principal = models.BooleanField(default=True, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_ean'


class PrecoLista(core.models.Log):
    """
    :Nome da classe/função: PrecoLista
    :descrição: Classe de lista de preços para referência de preços dos produtos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True, blank=True)
    dat_ini = models.DateField(null=True, blank=True)
    dat_fim = models.DateField(null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'preco_lista'

    def __str__(self):
        return self.nome


class ProdutoPreco(core.models.Log):
    """
    :Nome da classe/função: PrecoLista
    :descrição: Classe de relação entre produto e preço
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    precolista = models.ForeignKey('produto.PrecoLista', on_delete=models.DO_NOTHING, null=True, blank=True)
    desconto = models.ManyToManyField('produto.Desconto', through='produto.DescontoProdutoPreco', through_fields=('produtopreco', 'desconto'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_preco'


class TipoDesconto(core.models.Log):
    """
    :Nome da classe/função: TipoDesconto
    :descrição: Classe de tipos de descontos existentes
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=100, primary_key=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=10, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tipodesconto'


class Desconto(core.models.Log):
    """
    :Nome da classe/função: Desconto
    :descrição: Classe de descontos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    tipo = models.ForeignKey('produto.TipoDesconto', on_delete=models.DO_NOTHING, null=True, blank=True)
    qtd_ini_desc = models.IntegerField(null=True, blank=True)
    qtd_fim_desc = models.IntegerField(null=True, blank=True)
    valor_desc = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    per_desc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dat_ini = models.DateField(null=True, blank=True)
    dat_fim = models.DateField(null=True, blank=True)

    prioridade = models.IntegerField(null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_desconto'


class DescontoProdutoPreco(core.models.Log):
    """
    :Nome da classe/função: DescontoProdutoPreco
    :descrição: Classe de relação entre desconto e produtopreco
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    desconto = models.ForeignKey('produto.Desconto', on_delete=models.DO_NOTHING, null=True, blank=True)
    produtopreco = models.ForeignKey('produto.ProdutoPreco', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_descontoprodutopreco'


class Estoque(core.models.Log):
    """
    :Nome da classe/função: Estoque
    :descrição: Classe de estoque
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    quantidade = models.IntegerField(null=True, blank=True)
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_estoque'