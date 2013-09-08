from django.db import models
from django.db.models import signals
from django.conf import settings
from datetime import datetime
import xml.dom.minidom
import os
import requests

class Transaction(models.Model):


    STATUS_CRIADA = ('0','Criada')
    STATUS_ANDAMENTO = ('1','Andamento')
    STATUS_AUTENTICADA = ('2','Autenticada')
    STATUS_NAO_AUTENTICADA = ('3','N autenticada')
    STATUS_AUTORIZADA = ('4','Autorizada')
    STATUS_NAO_AUTORIZADA = ('5','N autorizada')
    STATUS_CAPTURADA = ('6','Capturada')
    STATUS_CANCELADA = ('9','Cancelada')
    STATUS_EM_AUTENTICACAO = ('10','Em autenticacao')
    STATUS_EM_CANCELAMENTO = ('12','Em cancelamento')
    STATUS_CHOICES = (
        STATUS_CRIADA,
        STATUS_ANDAMENTO,
        STATUS_AUTENTICADA,
        STATUS_NAO_AUTENTICADA,
        STATUS_AUTORIZADA,
        STATUS_NAO_AUTORIZADA,
        STATUS_CAPTURADA,
        STATUS_CANCELADA,
        STATUS_EM_AUTENTICACAO,
        STATUS_EM_CANCELAMENTO,        
    )
    
    tid = models.CharField('Tid',max_length=50)
    pedido = models.ForeignKey('pedido.Pedido',verbose_name='Pedido')
    valor = models.CharField('Valor',max_length=10)
    moeda = models.CharField('Moeda',max_length=4)
    data_criacao = models.DateTimeField('Data')
    bandeira = models.CharField('Bandeira do cartao',max_length=20)
    produto = models.CharField('Forma pagamento',max_length=50)
    parcelas = models.CharField('Parcelas',max_length=2)
    status = models.CharField('Status',choices=STATUS_CHOICES,max_length=30,default=0)
    capturada = models.BooleanField(default=False)
    
    autenticacao_codigo = models.CharField('Aut codigo',max_length=2, null=True, blank=True)
    autenticacao_mensagem = models.CharField('Mensagem',max_length=200, null=True, blank=True)
    autenticacao_data = models.DateTimeField('Data', null=True, blank=True)
    autenticacao_eci = models.CharField('Eci',max_length=10, null=True, blank=True)
    
    autorizacao_codigo = models.CharField('Codigo',max_length=2, null=True, blank=True)
    autorizacao_mensagem = models.CharField('Mensagem',max_length=200, null=True, blank=True)
    autorizacao_data = models.DateTimeField('Data', null=True, blank=True)
    autorizacao_lr = models.CharField('Lr',max_length=10, null=True, blank=True)
    autorizacao_nsu = models.CharField('Nsu',max_length=10, null=True, blank=True)
    
    captura_codigo = models.CharField('Codigo',max_length=2, null=True, blank=True)
    captura_mensagem = models.CharField('Mensagem',max_length=200, null=True, blank=True)
    captura_data = models.DateTimeField('Data', null=True, blank=True)


      
    # Signals
    def consultar(self):    
        if not self.capturada:        
            dados = {'affiliation_id':settings.CIELO_NUMERO,'api_key':settings.CIELO_TOKEN,'transaction_id':self.tid}        
            payload = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consulta.xml'), 'r').read() % dados
            response = requests.post('https://ecommerce.cbmp.com.br/servicos/ecommwsec.do', data={
                'mensagem': payload,
            })
            print response.content
            dom = xml.dom.minidom.parseString(response.content)
            
            if not dom.getElementsByTagName('erro'):
            
                status = int(dom.getElementsByTagName('status')[0].childNodes[0].data)
                
                self.status = status
                self.autenticacao_codigo = dom.getElementsByTagName('autenticacao')[0].getElementsByTagName('codigo')[0].childNodes[0].data
                self.autenticacao_mensagem = dom.getElementsByTagName('autenticacao')[0].getElementsByTagName('mensagem')[0].childNodes[0].data
                self.autenticacao_data = datetime.strptime(dom.getElementsByTagName('autenticacao')[0].getElementsByTagName('data-hora')[0].childNodes[0].data.split(".")[0],'%Y-%m-%dT%H:%M:%S')
                self.autenticacao_eci = dom.getElementsByTagName('autenticacao')[0].getElementsByTagName('eci')[0].childNodes[0].data
                
                self.autorizacao_codigo = dom.getElementsByTagName('autorizacao')[0].getElementsByTagName('codigo')[0].childNodes[0].data
                self.autorizacao_mensagem = dom.getElementsByTagName('autorizacao')[0].getElementsByTagName('mensagem')[0].childNodes[0].data
                self.autorizacao_data = datetime.strptime(dom.getElementsByTagName('autorizacao')[0].getElementsByTagName('data-hora')[0].childNodes[0].data.split(".")[0],'%Y-%m-%dT%H:%M:%S')
                self.autorizacao_lr = dom.getElementsByTagName('autorizacao')[0].getElementsByTagName('lr')[0].childNodes[0].data
                self.autorizacao_nsu = dom.getElementsByTagName('autorizacao')[0].getElementsByTagName('nsu')[0].childNodes[0].data
                
                if status == 6:
                    self.capturada = True                    
                    self.pedido.status = 3
                    self.pedido.save()   
                    self.captura_codigo = dom.getElementsByTagName('captura')[0].getElementsByTagName('codigo')[0].childNodes[0].data
                    self.captura_mensagem = dom.getElementsByTagName('captura')[0].getElementsByTagName('mensagem')[0].childNodes[0].data
                    self.captura_data = datetime.strptime(dom.getElementsByTagName('captura')[0].getElementsByTagName('data-hora')[0].childNodes[0].data.split(".")[0],'%Y-%m-%dT%H:%M:%S')                 
                    self.save()  
                self.save()
                
                                  
    
    def consultar_(self):         
        
        dados = {'affiliation_id':settings.CIELO_NUMERO,'api_key':settings.CIELO_TOKEN,'transaction_id':self.tid}        
        payload = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consulta.xml'), 'r').read() % dados
        response = requests.post('https://ecommerce.cbmp.com.br/servicos/ecommwsec.do', data={
            'mensagem': payload,
        })
        print response.content       
#signals.post_save.connect(capturar, sender=Transaction)
