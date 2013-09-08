# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('miniature.produto.views',
    
    url(r'^busca/$', 'busca', name='busca'),
    url(r'^mais-produtos/(?P<qtd_ini>[0-9]+)/(?P<qtd_fin>[0-9]+)/$', 'mais_produtos', name='mais_produtos'),
    url(r'^verificar-estoque/(?P<produto>[\w_-]+)/(?P<quantidade>[\w_-]+)/(?P<tamanho>[\w_-]+)/$', 'verificar_estoque', name='verificar_estoque'), 
    # exibicao do produto de uma categoria
    url(r'^(?P<categoria>[\w_-]+)/(?P<produto>[\w_-]+)/$', 'produto_detalhe', name='produto_detalhe'),     
    # listagem dos produtos de uma categoria
    url(r'^(?P<categoria>[\w_-]+)/$', 'produtos_lista', name='produtos_lista'),    
    url(r'^$', 'categorias_lista', name='categorias_lista' ),
    
    
       
        
)


