# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.cielo.models import Transaction

def consultar(modeladmin, request, queryset):
    for obj in queryset:
        obj.consultar()
consultar.short_description = "Consultar"

class AdminTransaction(admin.ModelAdmin):
    actions = [consultar]

admin.site.register(Transaction,AdminTransaction)
