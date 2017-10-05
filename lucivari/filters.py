#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:51:30 2017

@author: adamnicolaspelletier
"""

from django.contrib.auth.models import User
import django_filters

class ConditionFilter(django_filters.FilterSet):
    class Meta:
        model = Conditions
        fields = ['gene_symbol', 'cell_line', 'snv_id_no', ]