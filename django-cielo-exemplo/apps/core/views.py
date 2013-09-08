# -*- coding:utf-8 -*-
from django.template.loader import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from apps.produto.models import Produto

def homepage(request):         
    produtos = Produto.ativo.select_related()[:13]
    qtd = produtos.count()          
    return render_to_response('index.html', { 
        'produtos':produtos,
        'qtd':qtd,
    },context_instance=RequestContext(request))


