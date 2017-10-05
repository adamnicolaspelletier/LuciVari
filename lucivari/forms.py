#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 09:38:38 2017

@author: adamnicolaspelletier
"""

from django import forms
from django.contrib.auth.models import User
from lucivari.models import Experiment, Conditions, Snv, Genes, UserProfile
from lucivari.models import Document
#from validators import MimeTypeValidator



def get_cond_choices():
    condition_list = Conditions.objects.all()
    choices_list = []
    
    for i in condition_list:
        if i.gene in choices_list:
            pass
        else:   
            choices_list.append(i.gene_symbol)
            
    return choices_list    
    
    
#==============================================================================
# class ConditionForm(forms.ModelForm):
#     class Meta:
#         model = Conditions
#         
#       
#     def __init__(self, *args, **kwargs):
#         super(ConditionForm,self).__init__(*args,**kwargs)
#         self.fields['my_choice_field'] = forms.ChoiceField(
#                 choices=get_cond_choices() )
# 
#==============================================================================

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
        
        
#==============================================================================
# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, 
#                             help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=200, 
#                          help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Page
#         
#         # What fields do we want to include in our form?
#         # This way we don't need every field in the model present.
#         # Some fields may allow NULL values, so we may not want to include them.
#         # Here, we are hiding the foreign key.
#         # we can either exclude the category field from the form,
#         exclude = ('category',)
#         # or specify the fields to include (i.e. not include the category field)
#         #fields = ('title', 'url', 'views')
#     
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         url = cleaned_data.get('url')
#         
#         # If url is not empty and doesn't start with 'http://', 
#         # then prepend 'http://'.
#         if url and not url.startswith('http://'):
#             url = 'http://' + url
#             cleaned_data['url'] = url
#             
#             return cleaned_data
#==============================================================================
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        
