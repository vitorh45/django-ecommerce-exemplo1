# coding: utf-8
from django.shortcuts import redirect
from django.conf import settings

from apps.cielo.models import Transaction
from util import moneyfmt

from datetime import datetime
import os
import requests
import xml.dom.minidom
from decimal import Decimal
import urllib

SANDBOX_URL = 'https://qasecommerce.cielo.com.br/servicos/ecommwsec.do'
PRODUCTION_URL = 'https://ecommerce.cbmp.com.br/servicos/ecommwsec.do'


class GetAuthorizedException(Exception):
    def __init__(self, id, message=None):
        self.id = id
        self.message = message

    def __str__(self):
        return u'%s - %s' % (self.id, self.message)


class CaptureException(Exception):
    pass


class PaymentAttempt(object):
    VISA, MASTERCARD, DINERS, DISCOVER, ELO, AMEX = 'visa', 'mastercard', 'diners', 'discover', 'elo', 'amex'
    CARD_TYPE_C = (
        (VISA, u'Visa'),
        (MASTERCARD, u'Mastercard'),
        (DINERS, u'Diners'),
        (DISCOVER, u'Discover'),
        (ELO, u'ELO'),
        (AMEX, u'American express'),
    )

    CASH, INSTALLMENT_STORE, INSTALLMENT_CIELO = 1, 2, 3
    TRANSACTION_TYPE_C = (
        (CASH, u'À vista'),
        (INSTALLMENT_STORE, u'Parcelado (estabelecimento)'),
        (INSTALLMENT_CIELO, u'Parcelado (Cielo)'),
    )

    def __init__(self):

        self.url = SANDBOX_URL if settings.CIELO_SANDBOX else PRODUCTION_URL        
        self.affiliation_id = settings.CIELO_NUMERO
        self.api_key = settings.CIELO_TOKEN
        
    def transaction(self, total, card_type, installments, order, url_retorno, transaction=CASH):
        
        self.card_type = card_type
        self.transaction = transaction
        self.transaction_type = transaction  # para manter assinatura do pyrcws
        self.total = moneyfmt(total, sep='', dp='')
        self.installments = installments
        self.order_id = order.numero
        self.url_retorno = url_retorno  
        self.date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')        
        payload = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'authorize.xml'), 'r').read() % self.__dict__        
        response = requests.post(self.url, data={
            'mensagem': payload,
        })
        
        dom = xml.dom.minidom.parseString(response.content)
        
        if dom.getElementsByTagName('erro'):  
            error_id = dom.getElementsByTagName('erro')[0].getElementsByTagName('codigo')[0].childNodes[0].data          
            error_message = dom.getElementsByTagName('erro')[0].getElementsByTagName('mensagem')[0].childNodes[0].data 
            raise GetAuthorizedException(error_id, error_message)
        else:
            redirect_url = dom.getElementsByTagName('url-autenticacao')[0].childNodes[0].data
            status = int(dom.getElementsByTagName('status')[0].childNodes[0].data)

        tid = dom.getElementsByTagName('tid')[0].childNodes[0].data
        valor = dom.getElementsByTagName('dados-pedido')[0].getElementsByTagName('valor')[0].childNodes[0].data
        moeda = dom.getElementsByTagName('dados-pedido')[0].getElementsByTagName('moeda')[0].childNodes[0].data
        data = datetime.strptime(dom.getElementsByTagName('dados-pedido')[0].getElementsByTagName('data-hora')[0].childNodes[0].data.split(".")[0],'%Y-%m-%dT%H:%M:%S')
        bandeira = dom.getElementsByTagName('forma-pagamento')[0].getElementsByTagName('bandeira')[0].childNodes[0].data
        produto = dom.getElementsByTagName('forma-pagamento')[0].getElementsByTagName('produto')[0].childNodes[0].data
        parcelas = dom.getElementsByTagName('forma-pagamento')[0].getElementsByTagName('parcelas')[0].childNodes[0].data
        transaction = Transaction(tid=tid,pedido=order,valor=valor,moeda=moeda,data_criacao=data,bandeira=bandeira,produto=produto,parcelas=parcelas)
        transaction.save()              
        return redirect_url

    def capture(self, transaction_id):        
        self.transaction_id = transaction_id        
        payload = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'capture.xml'), 'r').read() % self.__dict__
        response = requests.post(self.url, data={
            'mensagem': payload,
        })        
        dom = xml.dom.minidom.parseString(response.content)
        status = int(dom.getElementsByTagName('status')[0].childNodes[0].data)
        if status != 6:            
            raise CaptureException()
        return True

