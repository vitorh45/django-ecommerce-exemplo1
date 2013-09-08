# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.produto.models import Produto, Categoria, Tamanho, ImagemProduto
from apps.produto.forms import ProdutoForm

class AdminInlineTamanho(admin.TabularInline):
    extra = 1
    model = Tamanho    

class AdminInlineImagemProduto(admin.TabularInline):
    extra = 1
    model = ImagemProduto
    
class AdminCategoria(admin.ModelAdmin):
    def imagem(obj):
        return "<img src='%s' width='200'>" % (obj.imagem.url)
    imagem.allow_tags = True    
    
    list_display = ('nome','slug', imagem)
    
class AdminProduto(admin.ModelAdmin):
    def imagem(obj):
        return "<img src='%s' width='100'>" % (obj.imagem_principal.url)
    imagem.allow_tags = True 
    
    def tamanhos_estoque(obj):
        content = ""
        for tam in obj.tamanhos.all():
            content += "%s - %s <br>" % (tam.sigla,tam.quantidade_estoque)
        return content
    
    tamanhos_estoque.short_description = "Tamanhos/Estoque"
    tamanhos_estoque.allow_tags = True
    
    list_display = ('nome', 'categoria', 'preco', 'em_promocao', 'preco_promocao', 'is_ativo', tamanhos_estoque, 'data_criacao', imagem)
    ordering = ('-data_criacao', 'nome')
    search_fields = ['nome']
    list_filter = ('categoria', 'em_promocao', 'is_ativo')
    inlines = [AdminInlineTamanho,AdminInlineImagemProduto]
    form = ProdutoForm

admin.site.register(Categoria,AdminCategoria)
admin.site.register(Produto,AdminProduto)
