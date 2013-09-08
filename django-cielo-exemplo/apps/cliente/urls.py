# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import * 
from django.contrib.auth.forms import *

urlpatterns = patterns('apps.cliente.views',    
    url(r'^$', 'detalhe', name='detalhe' ),
    url(r'^criar-nova-conta/$', 'cadastro', name='cadastro' ),
    url(r'^alterar-dados/$', 'alterar', name='alterar' ),    
    url(r'^entrar/$', 'login', name="entrar"),
    url(r'^sair/$', 'logout', name="sair"),
    url(r'^alterar-senha/$', password_change, {'template_name': 'cliente/password_change_form.html'}, name="alterar_senha"),
    url(r'^alterar-senha/confirma/$', password_change_done, {'template_name': 'cliente/password_change_done.html'} ),
    url(r'^recuperar-senha/$', password_reset, {'template_name': 'cliente/password_reset_form.html'}, name="recuperar_senha"),
    url(r'^recuperar-senha/confirma/$', password_reset_done, {'template_name': 'cliente/password_reset_done.html'}),
    url(r'^recuperar/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'cliente/password_reset_confirm.html'}),
    url(r'^recuperar/confirmar/$', password_reset_complete, {'template_name': 'cliente/password_reset_complete.html'}),    
    #pedidos     
    url(r'^meus-pedidos/(?P<numero>[0-9]+)/$', 'pedido_detalhe', name='pedido_detalhe' ),
    url(r'^meus-pedidos/$', 'pedidos', name='pedidos' ),    
    # enderecos
    url(r'^enderecos/$', 'enderecos_lista', name='enderecos_lista' ),  
    url(r'^adicionar-endereco/$', 'adicionar_endereco', name='adicionar_endereco' ),      
    url(r'^editar-endereco/(?P<id>[0-9]+)/$', 'editar_endereco', name='editar_endereco' ),
    url(r'^consultar-endereco/(?P<cep>[0-9]+)/$', 'consultar_endereco', name='consultar_endereco' ),                
)


