#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:46:53 2017

@author: adamnicolaspelletier
"""

from django.conf.urls import url
from lucivari import views
from django.conf import settings

from django.contrib import admin
from registration.backends.simple.views import RegistrationView
    

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/lucivari/'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'data_transform/$', views.data_transform, name='data_transform'),
    url(r'model_form_upload/$', views.model_form_upload, name='model_form_upload'),
    url(r'report_gen/$', views.report_gen, name='report_gen'),
    url(r'report_download/$', views.report_download, name='report_download'),
    url(r'zip_download/$', views.zip_download, name='zip_download'),
    url(r'static_file_download/$', views.static_file_download, name='static_file_download'),
    url(r'consol_upload/$', views.consol_upload, name='consol_upload'),
    url(r'consol_upload_part2/$', views.consol_upload_part2, name='consol_upload_part2'),
    url(r'consol_gen/$', views.consol_gen, name='consol_gen'),
    url(r'consol_download/$', views.consol_download, name='consol_download'),
    #url(r'register/$', views.register, name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^register_profile/$', views.register_profile, name='register_profile'),
    #url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    #url(r'simple_upload/$', views.simple_upload, name='simple_upload'),
#==============================================================================
#     url(r'^add_category/$', views.add_category, name='add_category'),
#     
#     url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
#         views.show_category,
#         name='show_category'),
#     url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
#         views.add_page,
#         name='add_page'),  
#     url(r'^restricted/', views.restricted, name='restricted'),
#     url(r'^goto/$', views.track_url, name='goto'),
     
#     url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
#     url(r'^profiles/$', views.list_profiles, name='list_profiles'),
#     url(r'^like_category/$', views.like_category, name='like_category'),
#     url(r'^suggest/$', views.suggest_category, name='suggest_category'),
#     url(r'^add/$', views.auto_add_page, name='auto_add_page'),
#==============================================================================
]
