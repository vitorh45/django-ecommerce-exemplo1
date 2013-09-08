# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.utils import simplejson
from django.core.mail.message import EmailMessage
from django.conf import settings
from apps.cliente.models import Cliente, Endereco
from apps.cliente.forms import CadastroForm, LoginForm, EnderecoForm
from apps.pedido.models import Pedido
from apps.produto.models import Tamanho, Produto
from cep import Correios

@csrf_protect
@never_cache
def login(request,template_name="cliente/login.html"):
    redirect_to = request.GET.get('next', request.META.get('HTTP_REFERER', '') )    
    if not request.user.is_authenticated():
        form = LoginForm(request.POST or None)
        if form.login(request):                
            return HttpResponseRedirect(redirect_to)        
        return render_to_response(template_name, {
            'form':form,
        },context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")
    
@login_required
def logout(request):    
    cart_id = request.session.get("CART-ID")
    auth_logout(request)
    request.session["CART-ID"] = cart_id    
    return HttpResponseRedirect("/")
    
@login_required
def detalhe(request):
    lista_desejo = get_lista_desejo(request)
    return render_to_response('cliente/detalhe.html', {            
        'lista_desejo':lista_desejo,    
    },context_instance=RequestContext(request))
    
def cadastro(request):
    if not request.user.is_authenticated():        
        form = CadastroForm(request.POST or None)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(reverse('homepage'))
        
        return render_to_response('cliente/cadastro.html', {
            'form':form,
        },context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('homepage'))

def alterar(request):
    if not request.user.is_authenticated():        
        form = CadastroForm(request.POST or None)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(reverse('homepage'))
        
        return render_to_response('cliente/cadastro.html', {
            'form':form,
        },context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('homepage'))
        
        
@login_required        
def pedidos(request):    
    pedidos = Pedido.ativados.select_related().filter(cliente__user=request.user)    
    return render_to_response('pedido/pedidos.html', {
        'pedidos':pedidos,
    },context_instance=RequestContext(request))

@login_required        
def pedido_detalhe(request,numero):
    pedido = get_object_or_404(Pedido.ativados.select_related(),cliente__user=request.user,numero=numero)    
    return render_to_response('pedido/pedido_detalhe.html', {
        'pedido':pedido,
    },context_instance=RequestContext(request))
    
@login_required        
def enderecos_lista(request): 
    enderecos = Endereco.objects.select_related().filter(cliente__user=request.user) 
    return render_to_response('cliente/enderecos_lista.html', {
        'enderecos':enderecos,
    },context_instance=RequestContext(request))

@login_required        
def adicionar_endereco(request):     
    redirect_to = request.GET.get('next', request.META.get('HTTP_REFERER', '') )         
    form = EnderecoForm(request.POST or None)    
    if form.is_valid():        
        form.save(request)                  
        return HttpResponseRedirect(redirect_to)       
    return render_to_response('cliente/adicionar_endereco.html', {
        'form':form,
        'endereco_tipo':'Preencha o formulario para adicionar um endereco',
        'endereco_breadcumb':'Adicionar endereco',
    },context_instance=RequestContext(request))

@login_required        
def editar_endereco(request,id): 
    endereco = get_object_or_404(Endereco,id=id,cliente__user=request.user)        
    form = EnderecoForm(request.POST or None, instance=endereco)
    if form.is_valid():
        form.save(request)        
        return HttpResponseRedirect(reverse("enderecos_lista"))    
    return render_to_response('cliente/adicionar_endereco.html', {
        'form':form,
        'endereco_tipo':'Altere os campos do seu endereco',
        'endereco_breadcumb':'Editar endereco',
    },context_instance=RequestContext(request))
    
def consultar_endereco(request,cep):
    if request.is_ajax():            
        c = Correios()
        try:
            dados = c.consulta(cep)[0]
        except:
            dados = {'falha':u'Cep não encontrado'}        
        data = simplejson.dumps(dados, indent=2, ensure_ascii=False)            
        return HttpResponse(data, mimetype='text/javascript; charset=utf-8')
