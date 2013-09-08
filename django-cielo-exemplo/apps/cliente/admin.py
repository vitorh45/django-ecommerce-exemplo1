# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.cliente.models import Cliente, Endereco

class AdminCliente(admin.ModelAdmin):
    def enderecos(obj):        
        content = ""
        for end in obj.endereco_set.all():
            content += "<a href='%s'>%s</a> <br>" % (end.get_admin_url(),end)        
        return content
    enderecos.allow_tags = True 
    
    def pedidos(obj):        
        conteudo = ""        
        for pedido in obj.pedido_set.all():            
            conteudo += "<a href='%s'>%s</a> <br>" % (pedido.get_admin_url(),pedido.numero)  
           
        return conteudo
    pedidos.allow_tags = True 
       
    list_display = ("__unicode__","cpf","rg","telefone","celular",enderecos,pedidos)
    
class AdminEndereco(admin.ModelAdmin):
    list_display = ('rua','numero','bairro','cidade','cep')
    
admin.site.register(Cliente,AdminCliente)
admin.site.register(Endereco,AdminEndereco)
