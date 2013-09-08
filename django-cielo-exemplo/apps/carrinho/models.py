# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.formats import number_format

from apps.cart.models import Item, Cart

class Carrinho(Cart):
    pass
    

class CustomItem(Item):    
    size = models.CharField(verbose_name=_('tamanho'), max_length=2)
    
    def preco_total_formatado(self):
        return number_format(self.quantity * self.unity_price, 2)
    preco_total_formatado = property(preco_total_formatado)
    
    def preco_total(self):
        return self.quantity * self.unity_price
    preco_total = property(preco_total)
    
    def peso_total(self):
        return self.quantity * self.product.peso
    peso_total = property(peso_total)

    
