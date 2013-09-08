# -*- coding: utf-8 -*-
from django import template
from miniature.produto.models import Categoria,Produto

register = template.Library()

@register.simple_tag(takes_context=True)
def get_categorias(context):
    try: context['categorias'] = Categoria.objects.all()
    except: pass
    return ''
				
@register.simple_tag(takes_context=True)
def get_sexo(context,sexo):
    dict_sexo = {'menino':'<li class="sprite usado-menino">Menino</li>','menina':'<li class="sprite usado-menina">Menina</li>','bebe':'<li class="sprite usado-bebe">Bebê</li>'}
    try: context['sexo'] = dict_sexo.get(sexo)
    except: pass
    return ''
				
@register.simple_tag(takes_context=True)
def get_sexo_index(context,sexo):
    dict_sexo = {'menino':'<li class="sprite usado-menino indent">Menino</li>','menina':'<li class="sprite usado-menina indent">Menina</li>','bebe':'<li class="sprite usado-bebe indent">Bebê</li>'}
    try: context['sexo'] = dict_sexo.get(sexo)
    except: pass
    return ''				
