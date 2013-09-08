# -*- coding: utf-8 -*-
from django.db.models import signals
from apps.core.utils import unique_slugify

def create_slug(sender, instance, signal, *args, **kwargs):    
    if not instance.slug:        
        unique_slugify(instance, getattr(instance, instance.slug_from))   
    


