from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.utils.formats import number_format
from taggit.managers import TaggableManager
from os.path import splitext, split, join
from apps.core.signals import create_slug
from datetime import datetime

def slugify_file_name(instance, filename):    
    path, file_name = split(filename)    
    file_name, ext = splitext(file_name)
    return '/'.join(['produto/', slugify(file_name)+ext])
    
class Categoria(models.Model):

    nome = models.CharField('Nome',max_length=100,unique=True)
    slug = models.SlugField('Slug',max_length=150,editable=False)    
    imagem = models.ImageField('Imagem',max_length=400,upload_to=slugify_file_name) 
    
    slug_field_name = 'slug'
    slug_from = 'nome'
    
    def __unicode__(self):
        return self.nome

class ProdutoAtivoManager(models.Manager):
    def get_query_set(self):
        return super(ProdutoAtivoManager, self).get_query_set().filter(tamanhos__quantidade_estoque__gt=0,is_ativo=True).distinct()

class Produto(models.Model):

    categoria = models.ForeignKey(Categoria,verbose_name='Categoria')
    nome = models.CharField('Nome',max_length=100,unique=True)
    slug = models.SlugField('Slug',max_length=150,editable=False)
    descricao = models.TextField('Descricao')    
    imagem_principal = models.ImageField('Imagem principal',upload_to=slugify_file_name,max_length=400)    
    preco = models.DecimalField('Preco',max_digits=10, decimal_places=2)
    em_promocao = models.BooleanField('Esta em promocao?',default=False)
    preco_promocao = models.DecimalField('Preco em promocao',null=True,blank=True,max_digits=10, decimal_places=2)    
    peso = models.IntegerField('Peso em gramas')
    is_ativo = models.BooleanField('Esta ativo?',default=True)
    data_criacao = models.DateTimeField('Data de criacao',auto_now_add=True)
    data_alteracao = models.DateTimeField('Data alreracao',auto_now=True,editable=False)    
    objects = models.Manager()
    ativo = ProdutoAtivoManager()    
    tem_tamanho = models.BooleanField("Este produto possui tamanho?", default=True)    
    tags = TaggableManager(blank=True)
    
    slug_field_name = 'slug'
    slug_from = 'nome'

    def __unicode__(self):
        return self.nome

    class Meta:        
        ordering = ['-data_criacao']
    
    @property
    def valor_formatado_br(self):        
        return number_format(self.preco, 2) 
        
    @property
    def valor_formatado_br_promo(self):
        if self.em_promocao:
            return number_format(self.preco_promocao, 2)         
        else:
            return None
    
    @property
    def valor_formatado_ps(self):
        return number_format(self.preco, 2).replace('.','').replace(',','.') 
        
    @property
    def valor_formatado_ps_promo(self):
        if self.em_promocao:
            return number_format(self.preco_promocao, 2).replace('.','').replace(',','.')          
        else:
            return None 
        
class Tamanho(models.Model):
    
    produto = models.ForeignKey(Produto,verbose_name='Produto', related_name='tamanhos')
    sigla = models.CharField('Tamanho',max_length=2, default="U")    
    quantidade_estoque = models.PositiveIntegerField('Quantidade em estoque', default=0)
    
    def __unicode__(self):
        return self.sigla
    
    def save(self):
       self.sigla = self.sigla.upper()
       super(Tamanho, self).save()
    
class ImagemProduto(models.Model):
    
    produto = models.ForeignKey(Produto,verbose_name='Produto')
    nome = models.CharField('Nome da imagem',max_length=100)
    arquivo = models.ImageField('Imagem',upload_to=slugify_file_name,max_length=400)
    
    def __unicode__(self):
        return self.nome
        
# Signals
signals.post_save.connect(create_slug, sender=Categoria)
signals.post_save.connect(create_slug, sender=Produto)

