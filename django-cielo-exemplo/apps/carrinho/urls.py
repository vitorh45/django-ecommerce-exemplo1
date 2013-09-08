# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('apps.carrinho.views',
    
    url(r'^$', TemplateView.as_view(template_name="carrinho/exibir.html"), name='exibir'),    
    url(r'^adicionar-item/(?P<produto_id>[\w_-]+)/(?P<quantidade>[\w_-]+)/(?P<tamanho>[\w_-]+)/$', 'adicionar_item', name='adicionar_item'),
    #url(r'^adicionar-item/$', 'adicionar_item', name='adicionar_item'),
    url(r'^remover-item/(?P<produto_id>[\w_-]+)/(?P<tamanho>[\w_-]+)/$', 'remover_item', name='remover_item'),   
    url(r'^consultar-frete/(?P<cep>[0-9]+)/$', 'consultar_frete', name='consultar_frete'),  
    url(r'^finalizar-pagamento/escolher-endereco/$', 'finalizar_pagamento_escolher_endereco', name='finalizar_pagamento_escolher_endereco' ), 
    url(r'^finalizar-pagamento/resumo/$', 'finalizar_pagamento_resumo', name='finalizar_pagamento_resumo' ), 
    url(r'^finalizar-pagamento/escolher-forma-pagamento/$', 'finalizar_pagamento_escolher_forma_pagamento', name='finalizar_pagamento_escolher_forma_pagamento' ),  
    url(r'^finalizar-pagamento/$', 'finalizar_pagamento', name='finalizar_pagamento' ),        
    #url(r'^compra-finalizada/$', TemplateView.as_view(template_name="carrinho/compra_finalizada.html")),
    url(r'^compra-finalizada/(?P<tipo>[\w_-]+)/$', 'compra_finalizada', name='compra_finalizada'),
    url(r'^atualizar-item/(?P<produto_id>[\w_-]+)/(?P<tamanho>[\w_-]+)/(?P<quantidade>[\w_-]+)/$', 'atualizar_carrinho', name='atualizar_carrinho'),
    url(r'^estoque-indisponivel/$', TemplateView.as_view(template_name="carrinho/estoque_indisponivel.html"), name='estoque_indisponivel'),   
        
)


