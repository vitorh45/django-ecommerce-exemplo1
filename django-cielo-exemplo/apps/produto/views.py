# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.db.models import Q
from apps.produto.models import Produto,Categoria
from apps.carrinho.cart import Carrinho
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import sys,traceback

def categorias_lista(request):
    categorias = Categoria.objects.all()
    return render_to_response('produto/categorias_lista.html', { 
        'categorias':categorias,
    },context_instance=RequestContext(request))


def produtos_lista(request, categoria): 
    cat = get_object_or_404(Categoria,slug=categoria)
    produtos = Produto.ativo.select_related().filter(categoria=cat).order_by('data_criacao')[:7]        
    return render_to_response('produto/produtos_lista.html', {
        'produtos':produtos,
        'categoria':categoria, 
    },context_instance=RequestContext(request))

def produto_detalhe(request, categoria, produto):    
    produto = get_object_or_404(Produto,slug=produto, categoria__slug=categoria)        
    produtos_relacionados = produto.tags.similar_objects()[:7]        
    variaveis['produto'] = produto
    variaveis['produtos'] = produtos_relacionados
    return render_to_response('produto/produto_detalhe.html', variaveis,context_instance=RequestContext(request))

def verificar_estoque(request,produto,quantidade,tamanho):    
    if request.is_ajax():    
        try:      
            carrinho = Carrinho(request)
            produto = Produto.ativo.get(id=produto)
            tam = tamanho
            quantidade_item = carrinho.verificar_quantidade(produto,tam)
            tamanho = produto.tamanhos.get(sigla=tam)         
            output = {'ok':''}        
            if (int(quantidade) > tamanho.quantidade_estoque) or ((int(quantidade) + quantidade_item) > tamanho.quantidade_estoque):            
                output = {'error':"quantidade indisponivel em estoque"}
        except:
            pass
        data = simplejson.dumps(output, indent=2, ensure_ascii=False)            
        return HttpResponse(data, mimetype='text/javascript; charset=utf-8')
        
def busca(request):
    variaveis = {}
    termo = request.GET.get('q',None)     
    produtos = []  
    if termo:
        variaveis['termo'] = termo
        produtos = Produto.ativo.select_related().filter(Q(nome__icontains=termo) | Q(descricao__icontains=termo)).order_by('data_criacao')[:7]    
        variaveis['produtos'] = produtos
        if len(produtos) == 0:
            mensagem = 'Não foi encontrado nenhum produto.'
            variaveis['mensagem'] = mensagem
        return render_to_response('produto/busca.html', variaveis, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")
        
import traceback,sys 
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))   
def mais_produtos(request,qtd_ini,qtd_fin):
    id = request.GET.get("id",0)
    cat = request.GET.get("cat",None) 
    tipo = request.GET.get("tipo",None)   
           
    if cat:        
        if tipo:
            produtos = Produto.ativo.filter(categoria__slug=cat,tipo=tipo).select_related()[qtd_ini:qtd_fin]
        else:            
            produtos = Produto.ativo.filter(categoria__slug=cat).select_related()[qtd_ini:qtd_fin]     
    else:        
        if int(id) > 0:        
            produto = get_object_or_404(Produto,id=id)            
            produtos = produto.tags.similar_objects()[int(qtd_ini):int(qtd_fin)] 
        else:
            produtos = Produto.ativo.select_related()[qtd_ini:qtd_fin] 
    return Response({'produtos':produtos}, template_name='produto/produtos_lista.html')
