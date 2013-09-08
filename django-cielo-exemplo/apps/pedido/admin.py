# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.pedido.models import Pedido
from apps.produto.models import Produto, Tamanho
'''
class AdminInlineItemPedido(admin.TabularInline):
    extra = 1
    model = ItemPedido
'''
class AdminPedido(admin.ModelAdmin):

    def cancelar_pedido(modeladmin, request, queryset):
        for obj in queryset:
            for item in obj.carrinho.item_set.all():            
                produto = Produto.objects.get(id=item.produto.id)
                tamanho = Tamanho.objects.get(produto=produto,sigla=item.tamanho)        
                tamanho.quantidade_estoque += item.quantidade
                tamanho.save()
            obj.status = 7
            obj.save()   
    cancelar_pedido.short_description = "Cancelar pedido"

    def frete(obj):        
        return "%s/R$ %s" % (obj.get_tipo_frete_display(),obj.valor_frete)
    frete.short_description = "Frete/Valor"
    
    def itens(obj):
        content = ""
        for item in obj.carrinho.item_set.all():
            content += "%s / %s / %s / R$ %s <br>" % (item.product.nome, item.size, item.quantity, item.preco_total_formatado)
        return content
    itens.short_description = "Itens do pedido: nome / tam / qtd / valor"
    itens.allow_tags = True
    
    def valor_total(obj):
        return "R$ %s" % obj.valor_total_formatado
    
    list_display = ("__unicode__",'cliente',itens,frete,valor_total,'status','data_criacao','ativado') 
    actions = [cancelar_pedido,]

admin.site.register(Pedido,AdminPedido)

