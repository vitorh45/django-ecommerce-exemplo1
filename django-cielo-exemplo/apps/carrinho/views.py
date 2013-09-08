# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from apps.produto.models import Produto, Categoria, Tamanho
from apps.carrinho.cart import CustomCart as Carrinho
from apps.pedido.models import Pedido
from apps.pedido.ceps import CEPS_GRATIS
from apps.pedido.utils import enviar_email_confirmacao
from apps.cliente.models import Endereco, Cliente
from apps.cliente.forms import EnderecoForm
from apps.cielo import PaymentAttempt, GetAuthorizedException, CaptureException
from apps.cielo.models import Transaction
from apps.core.models import Config
from decimal import Decimal
import urllib2
import traceback,sys

def adicionar_item(request, produto_id, quantidade, tamanho): 
    produto = get_object_or_404(Produto,id=produto_id)
    carrinho = Carrinho(request)
    carrinho.add(produto, tamanho, quantidade)    
    return direct_to_template(request,template='carrinho/confirmacao_item_adicionado.html')

def remover_item(request, produto_id, tamanho):
    produto = Produto.objects.get(id=produto_id)
    carrinho = Carrinho(request)
    carrinho.remove(produto, tamanho)
    return HttpResponseRedirect(reverse('carrinho:exibir'))

def atualizar_carrinho(request, produto_id, tamanho, quantidade):
    redirect_to = request.GET.get('next', request.META.get('HTTP_REFERER', '') ) 
    produto = get_object_or_404(Produto,id=produto_id)
    carrinho = Carrinho(request)
    carrinho.update(produto, tamanho, quantidade)
    return HttpResponseRedirect(redirect_to)   

@login_required
def finalizar_pagamento_escolher_endereco(request): 
    enderecos = Endereco.objects.filter(cliente__user=request.user)
    endereco_form = EnderecoForm()    
    return render_to_response('carrinho/finalizar_pagamento_escolher_endereco.html', {  
        'enderecos':enderecos,  
        'form':endereco_form,     
    },context_instance=RequestContext(request))

@login_required
def finalizar_pagamento_resumo(request):    
    if request.method == "POST":        
        cliente = get_object_or_404(Cliente,user=request.user)
        endereco_form = EnderecoForm(request.POST)        
        if endereco_form.is_valid():            
            endereco, created = Endereco.objects.get_or_create(cliente=cliente,**endereco_form.cleaned_data) 
        else:
            return render_to_response('carrinho/finalizar_pagamento_escolher_endereco.html', {  
                'enderecos':Endereco.objects.filter(cliente__user=request.user),  
                'form':endereco_form,     
            },context_instance=RequestContext(request))
          
        request.session['endereco'] = endereco.id 
        carrinho = Carrinho(request) 
        return render_to_response('carrinho/finalizar_pagamento_resumo.html', {   
            'endereco':endereco,
        },context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('carrinho:finalizar_pagamento_escolher_endereco'))
        
@login_required
def finalizar_pagamento_escolher_forma_pagamento(request): 
    if verificar_estoque_produtos(request) > 0:
        return HttpResponseRedirect(reverse('carrinho:estoque_indisponivel'))
    if not request.session.get('endereco',False):
        return HttpResponseRedirect(reverse('carrinho:finalizar_pagamento_escolher_endereco'))    
    frete_valor,frete_tipo,frete_tipo_nome = request.POST.get('tipo-frete',None).split("/")  
    request.session['frete'] = request.POST.get('tipo-frete',None)
    carrinho = Carrinho(request) 
    valor_compra = Decimal(frete_valor) + carrinho.preco_total()
    return render_to_response('carrinho/finalizar_pagamento_escolher_forma_pagamento.html', {  
        'valor_compra':valor_compra,
    },context_instance=RequestContext(request))

@login_required
def finalizar_pagamento(request):
    if verificar_estoque_produtos(request) > 0:
        return HttpResponseRedirect(reverse('carrinho:estoque_indisponivel'))
    if not request.session.get('endereco',False):
        return HttpResponseRedirect(reverse('carrinho:finalizar_pagamento_escolher_endereco'))       
    opcao_pagamento = request.POST.get('opcao-pagamento',None)
    if not opcao_pagamento:         
        return retornar_escolha_pagamento(request,u"Ocorreu algum problema no pagamento. Por favor tente realizar o pagamento novamente.")    
    carrinho = Carrinho(request)    
    endereco = get_object_or_404(Endereco, id=request.session['endereco'])
    frete_valor, frete_tipo, frete_tipo_nome = request.session['frete'].split("/")    
    valor_compra = Decimal(frete_valor)  + carrinho.preco_total()            
    valor_compra = str(valor_compra).replace(",",".") 
        
    if opcao_pagamento == "cielo":
                    
        bandeira = request.POST['bandeira']
        prestacoes = int(request.POST['prestacoes'])                        
        pedido,created = Pedido.objects.get_or_create(cliente=Cliente.objects.get(user=request.user),carrinho=carrinho,endereco=endereco,tipo_frete=frete_tipo,frete=frete_valor,tipo_pagamento=opcao_pagamento,para_presente=para_presente,presente_de=presente_de,presente_para=presente_para)        
        if created:
            atualizar_estoque(pedido)
        payment = PaymentAttempt()            
        if prestacoes > 1:
            transaction = 2
        else:
            transaction = 1 
        try:                
            return redirect(payment.transaction(total=Decimal(valor_compra),card_type=bandeira,order=pedido,installments=prestacoes,transaction=transaction,url_retorno="http://www.miniature.com.br/carrinho/compra-finalizada/cielo/?p=%s" % pedido.numero))
        except:
            messages.error(request,"Ocorreu algum problema na tentativa de pagamento com cartão de crédito através da Cielo. Por favor tente realizar o pagamento novamente.")
            return render_to_response('carrinho/finalizar_pagamento_escolher_forma_pagamento.html', {  
                'valor_compra':valor_compra.replace(".",','),
            },context_instance=RequestContext(request))
                
         
def compra_finalizada(request,tipo):
    try:
        del request.session['presente_para']
        del request.session['presente_de']
        del request.session['para_presente']
        del request.session['endereco']
        del request.session['frete']
        del request.session['CART-ID']
    except:
        pass
    pedido = get_object_or_404(Pedido,numero=request.GET['p'])    
    pedido.ativado = True
    pedido.save()    
    mensagem = None 
    transacao = Transaction.objects.get(pedido=pedido)
    transacao.consultar()
    mensagem = transacao.autorizacao_mensagem           
    return render_to_response('carrinho/compra_finalizada.html', {   
        'pedido': pedido,
        'mensagem': mensagem,         
    },context_instance=RequestContext(request))
                    
def verificar_estoque_produtos(request):    
    carrinho = Carrinho(request)
    for item in carrinho:
        quantidade_estoque = item.produto.tamanhos.get(sigla=item.tamanho).quantidade_estoque
        quantidade_carrinho = item.quantidade        
        if quantidade_carrinho > quantidade_estoque:
            messages.error(request, u'O produto "%s" não possui %s unidade(s) em estoque. Possui %s unidade(s).' % (item.produto.nome,quantidade_carrinho,quantidade_estoque))    
            if quantidade_estoque == 0:
                carrinho.remove(item.produto,item.tamanho)
            else:
                carrinho.update(item.produto,item.tamanho,quantidade_estoque)
    return len(messages.get_messages(request)._queued_messages)
 
