# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.localflavor.br.forms import BRCPFField
from datetime import datetime
from apps.cliente.models import Cliente, Endereco
from apps.carrinho.cart import CustomCart as Carrinho
import random, hashlib

class CadastroForm(forms.Form):
    
    nome = forms.CharField(label=u"Nome")
    sobrenome = forms.CharField(label=u"Sobrenome")
    email = forms.EmailField(label="Email")
    senha1 = forms.CharField(label=u"Senha", help_text = u'A senha deve conter seis caracteres ou mais.', widget=forms.PasswordInput)
    senha2 = forms.CharField(label=u"Confirmar senha", widget=forms.PasswordInput,help_text = u"Entre com a mesma senha, para verificação.")
    cpf = BRCPFField(label='CPF',max_length=14)
    rg = forms.CharField(label='RG',max_length=10) 
    telefone = forms.CharField(label='Telefone',max_length=13) 
    celular = forms.CharField(label='Celular',max_length=13, required=False) 

    class Meta:
        model = Cliente        
        exclude = ("user")
        #fields = ("first_name","last_name","email","senha1","senha2","cpf","rg","telefone","celular")
    
    def clean_senha1(self):
        password1 = self.cleaned_data.get('senha1', '')
        if len(password1) < 6:
            raise forms.ValidationError("A senha deve conter seis caracteres ou mais.")
        return password1

    def clean_senha2(self):
        password1 = self.cleaned_data.get('senha1', '')
        password2 = self.cleaned_data.get('senha2', '')
        if len(password2) < 6:
            raise forms.ValidationError("A senha deve conter seis caracteres ou mais.")
        if password1 != password2:
            raise forms.ValidationError("As duas senhas não conferem.")
        return password2

    def clean_email(self):
        if len(self.cleaned_data['email']) == 0:
            raise forms.ValidationError(u"Este campo é obrigatório.")
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(u"Esse e-mail já está em uso. Por favor escolha outro.")
        return self.cleaned_data['email']

    def save(self,request,commit=True):
        
        first_name = self.cleaned_data['nome']
        last_name = self.cleaned_data['sobrenome']
        username = self.cleaned_data['email']        
        password = self.cleaned_data['senha1']
        email = username
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        cpf = self.cleaned_data.get('cpf')
        rg = self.cleaned_data.get('rg')
        telefone = self.cleaned_data.get('telefone')
        celular = self.cleaned_data.get('celular',None)        
        cliente = Cliente.objects.create(user=user,cpf=cpf,rg=rg,telefone=telefone,celular=celular)
        cliente.save()
        
        
        login(request, authenticate(username=username, password=password))
                
class EnderecoForm(forms.ModelForm):
                
    class Meta:
        model = Endereco
        exclude = ("cliente")
        
    def save(self,request,commit=True):
        end = super(EnderecoForm, self).save(commit=False)
        self.instance.cliente = Cliente.objects.get(user=request.user)
        if commit:
            end.save()
        return end     
            
class LoginForm(forms.Form):
    
    email = forms.EmailField(label="Email", max_length=30, widget=forms.TextInput(attrs={'class':'validate[required] text-input'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'validate[required] text-input'}))
    lembrar = forms.BooleanField(label="Continuar logado", required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(u"Email ou senha inválidos")

        return self.cleaned_data
    
    def login(self, request):
        if self.is_valid():                      
            login(request, authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])) 
            if self.cleaned_data['lembrar']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False




