from django.db import models
from datetime import datetime
from django.db.models import signals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Cliente(models.Model):

    user = models.OneToOneField(User)
    cpf = models.CharField('CPF',max_length=14)
    rg = models.CharField('RG',max_length=10)    
    telefone = models.CharField('Telefone',max_length=13) 
    celular = models.CharField('Celular',max_length=13,null=True,blank=True) 
      
    def __unicode__(self):
        return self.user.get_full_name()

STATE_CHOICES = (
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
)
class Endereco(models.Model):
    
    cliente = models.ForeignKey(Cliente,verbose_name="Cliente")
    rua = models.CharField("Rua",max_length=100)
    numero = models.IntegerField("Numero",max_length=100)
    complemento = models.CharField("Complemento",max_length=100,null=True,blank=True)
    bairro = models.CharField("Bairro",max_length=100)
    cidade = models.CharField("Cidade",max_length=100)
    estado = models.CharField("Estado",choices=STATE_CHOICES,max_length=2)
    cep = models.CharField("Cep",max_length=8)
    
    def __unicode__(self):
        return "%s, %s - %s" % (self.rua,self.numero,self.cep)
    
    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.module_name), args=(self.pk,)) 
