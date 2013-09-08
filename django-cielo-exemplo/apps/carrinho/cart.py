# -*- coding: utf-8 -*-
import datetime
import models
from django.utils.formats import number_format

from apps.cart import Cart as Cart_
from apps.cart.models import Cart, Item


class CustomCart(Cart_):    

    def add(self, product, size, quantity=1):        
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
                size=size,                
            )
            item.quantity += quantity
            item.save()
        except models.Item.DoesNotExist:            
            item = models.Item()
            item.cart = self.cart
            item.product = product                        
            item.quantity = quantity
            item.size = size
            if product.em_promocao:
                item.unity_price = product.preco_promocao
            else:
                item.unity_price = produto.preco            
            item.save()
          
    def verificar_quantidade(self,produto,tamanho):
        try:
            item = models.Item.objects.get(carrinho=self.carrinho,produto=produto,tamanho=tamanho)
            return item.quantidade
        except:
            return 0
             
    def preco_total(self):
        total = 0
        for item in models.Item.objects.select_related().filter(carrinho=self.carrinho):            
            total += item.preco_total
        return total
        
    def preco_total_formatado(self):
        total = 0
        for item in models.Item.objects.select_related().filter(carrinho=self.carrinho):            
            total += item.preco_total
        return number_format(total,2)
        
    def peso_total(self):
        total = 0
        for item in models.Item.objects.select_related().filter(carrinho=self.carrinho):
            total += item.product.peso * item.quantity
        return total
        
    def quantidade(self):
        quantidade = len(self.cart.item_set.all())
