# coding: utf-8
from django import forms
from apps.produto.models import Produto

class ProdutoForm(forms.ModelForm):

    preco = forms.DecimalField(label="Preco",max_digits=10, decimal_places=2, localize=True)
    preco_promocao = forms.DecimalField(label="Preco",max_digits=10, decimal_places=2, localize=True, required=False)
    
    class Meta:
        model = Produto
