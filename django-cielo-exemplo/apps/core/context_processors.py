# coding: utf-8
from django.conf import settings
from apps.carrinho.cart import CustomCart as Carrinho

def carrinho(request):    
    carrinho = Carrinho(request)          
    return {
        'carrinho_qtd_itens': carrinho.quantidade(),
        'carrinho':carrinho,
    }

