# coding: utf-8
from django.db import models
from django.utils.formats import number_format
from django.db.models import signals
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from apps.cliente.models import Cliente
from apps.carrinho.models import Carrinho, Item
from apps.produto.models import Produto, Tamanho
from datetime import datetime
from time import time


class PedidoAtivadoManager(models.Manager):
    def get_query_set(self):
        return super(PedidoAtivadoManager, self).get_query_set().filter(ativado=True)
        
class Pedido(models.Model):
    
    TIPOS_FRETE_PAC = (1,u'PAC')
    TIPOS_FRETE_SEDEX = (2,u'Sedex')
    TIPOS_FRETE_FREE = (3,u'Gratis(PAC)')
    TIPOS_FRETE_MOTOBOY = (4,u'Gratis(motoboy)')
    TIPOS_FRETE = (
        TIPOS_FRETE_PAC,
        TIPOS_FRETE_SEDEX,
        TIPOS_FRETE_FREE,  
        TIPOS_FRETE_MOTOBOY,      
    )
    
    numero = models.CharField('Numero do pedido',max_length=10,null=True)
    cliente = models.ForeignKey('cliente.Cliente',verbose_name='Cliente')    
    carrinho = models.ForeignKey('carrinho.Carrinho',verbose_name='Carrinho')    
    endereco = models.ForeignKey('cliente.Endereco',verbose_name='Endereco',null=True)
    tipo_frete = models.IntegerField('Frete',choices=TIPOS_FRETE,default=1,max_length=1)
    frete = models.DecimalField('Valor do frete',max_digits=10,decimal_places=2, blank=True, null=True)   
    data_criacao = models.DateTimeField(default=datetime.now)
    data_alteracao  = models.DateTimeField(default=datetime.now)
        
    status = models.IntegerField('Status do Pedido', default=1,max_length=1)
    codigo_rastreio = models.CharField(u'Código de rastreio',max_length=30,null=True,blank=True)
    email_confirmacao_enviado = models.BooleanField('Email de confirmação enviado?', default=False)
    ativado = models.BooleanField(u'Se o pedido foi ativado. Se o usuario foi levado a pagina da cielo ou pagseguro para pagar',default=False)
    
    objects = models.Manager()
    ativados = PedidoAtivadoManager()
    
    def __unicode__(self):
        return self.numero
   
    class Meta:
        ordering = ['-data_criacao']            
                
    def valor_total(self):
        valor = 0
        for item in self.carrinho.item_set.all():
            valor += item.preco_total
        return self.frete + valor        
    valor_total = property(valor_total)
    
    def valor_total_formatado(self):        
        return number_format(self.valor_total, 2)         
    valor_total_formatado = property(valor_total_formatado)
    
    @property
    def valor_frete(self):
        return number_format(self.frete, 2) 
        
    def get_admin_url(self):            
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.module_name), args=(self.pk,)) 
        
# Signals
def criar_numero(sender, instance, signal, *args, **kwargs): 
    if not instance.numero:        
        instance.numero = "%09d" % instance.id
        instance.save()                   

signals.post_save.connect(criar_numero, sender=Pedido)
