from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import User


import os
#from django.template.defaultfilters import slugify
#from django.contrib.auth.models import User
#from django import forms



class Genes(models.Model):
    gene_symbol = models.TextField(db_column='Gene_Symbol', blank=True, primary_key=True)  # Field name made lowercase.
    chr = models.TextField(db_column='Chr', blank=True, null=True)  # Field name made lowercase.
    gene_start_pos = models.IntegerField(db_column='Gene_Start_Pos', blank=True, null=True)  # Field name made lowercase.
    gene_stop_pos = models.IntegerField(db_column='Gene_Stop_Pos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'genes'
        verbose_name_plural = 'Genes'
        
        
    def __str__(self): #For Python2, use __unicode__too
        return self.gene_symbol
    
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.gene_symbol)

class Snv(models.Model):
    snv_id_no = models.IntegerField(db_column='SNV_ID_NO', blank=True, primary_key=True)  # Field name made lowercase.
    gene_symbol = models.ForeignKey(Genes, db_column='Gene_Symbol')  # Field name made lowercase.
    chr = models.TextField(db_column='Chr', blank=True, null=True)  # Field name made lowercase.
    variant_status = models.TextField(db_column='Variant_status', blank=True, null=True)  # Field name made lowercase.
    snv = models.TextField(db_column='SNV', blank=True, null=True)  # Field name made lowercase.
    snv_pos = models.TextField(db_column='SNV_pos', blank=True, null=True)  # Field name made lowercase.
    sift_score = models.TextField(db_column='SIFT_SCORE', blank=True, null=True)  # Field name made lowercase.
    polyphen_score = models.TextField(db_column='Polyphen_SCORE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SNV'
        verbose_name_plural = 'Snvs'
    
    def __str__(self): #For Python2, use __unicode__too
        return self.snv_id_no
    
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.snv_id_no)

class Conditions(models.Model):
    condition_id = models.IntegerField(db_column='Condition_ID', blank=True, primary_key=True)  # Field name made lowercase.
    condition_group = models.IntegerField(db_column='Condition_Group', blank=True, null=True)  # Field name made lowercase.
    gene_symbol = models.ForeignKey(Genes, db_column='Gene_Symbol')  # Field name made lowercase.
    cell_line = models.TextField(db_column='Cell_line', blank=True, null=True)  # Field name made lowercase.
    ff_average = models.FloatField(db_column='FF_Average', blank=True, null=True)  # Field name made lowercase.
    ff_std = models.FloatField(db_column='FF_STD', blank=True, null=True)  # Field name made lowercase.
    rn_average = models.FloatField(db_column='RN_Average', blank=True, null=True)  # Field name made lowercase.
    rn_std = models.FloatField(db_column='RN_STD', blank=True, null=True)  # Field name made lowercase.
    rlu_average = models.FloatField(db_column='RLU_Average', blank=True, null=True)  # Field name made lowercase.
    rlu_std = models.FloatField(db_column='RLU_STD', blank=True, null=True)  # Field name made lowercase.
    fc_average = models.FloatField(db_column='FC_Average', blank=True, null=True)  # Field name made lowercase.
    fc_std = models.FloatField(db_column='FC_STD', blank=True, null=True)  # Field name made lowercase.
    snv_id_no = models.ForeignKey(Snv, db_column='SNV_ID_NO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'conditions'
        verbose_name_plural = 'Conditions'
        
    def __str__(self): #For Python2, use __unicode__too
        return self.condition_id
    
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.condition_id)
        
        
class Experiment(models.Model):
    id = models.TextField(db_column='ID', blank=True, primary_key=True)  # Field name made lowercase.
    gene_symbol = models.ForeignKey(Genes, db_column='Gene_Symbol')  # Field name made lowercase.
    replicate = models.TextField(db_column='Replicate', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    experiment_number = models.IntegerField(db_column='Experiment_number', blank=True, null=True)  # Field name made lowercase.
    condition_id = models.ForeignKey(Conditions, db_column='Condition_ID')  # Field name made lowercase.
    condition_group = models.IntegerField(db_column='Condition_Group', blank=True, null=True)  # Field name made lowercase.
    ff_value = models.FloatField(db_column='FF_Value', blank=True, null=True)  # Field name made lowercase.
    rn_value = models.FloatField(db_column='RN_Value', blank=True, null=True)  # Field name made lowercase.
    rlu_value = models.FloatField(db_column='RLU_Value', blank=True, null=True)  # Field name made lowercase.
    rlu_wt = models.FloatField(db_column='RLU_WT', blank=True, null=True)  # Field name made lowercase.
    fold_change = models.FloatField(db_column='Fold_Change', blank=True, null=True)  # Field name made lowercase.
    snv_id_no = models.ForeignKey(Snv, db_column='SNV_ID_NO')  # Field name made lowercase.
  
    class Meta:
        managed = False
        db_table = 'experiment'   

    def __str__(self): #For Python2, use __unicode__too
        return self.id
    
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.id)
    

class content_file_generic(models.Model):
    generic = models.TextField(db_column='filename', blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'generic'   
    
    def __str__(self):
        return self.description
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.description)
    
    

def content_file_name(instance, filename):
    instance.original_file_name = filename
    #newname = request.session['upload_file']
    newname = content_file_generic.generic
    return os.path.join('documents', newname)    
    
    
class Document(models.Model):
    #document = models.FileField(upload_to=content_file_name)
    document = models.FileField(upload_to='documents/')
    original_file_name = models.CharField(editable=False, max_length=255)
    pdffilename = models.CharField(max_length=255, blank=True)  
    reportfilename = models.CharField(max_length=255, blank=True)
    generic_filename = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.document.name
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.document.name)

    def save(self, *args, **kwargs):
        self.slug = self.document.name
        super(Document, self).save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        #os.remove(os.path.join(settings.MEDIA_ROOT,self.document.name))
        super(Document,self).delete(*args,**kwargs)
        
        
class TemplateFile(models.Model):
    filename = models.TextField(db_column='filename', blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'templates'   
    
    def __str__(self):
        return self.description.name
    
    def __unicode__(self): #For Python2, use __unicode__too
        return str(self.description.name)


#==============================================================================
# def content_file_name(instance, filename):
#     aggreg_filename = "lucif_aggreg_file.txt" 
#     return os.path.join('documents', filename) 
# 
# class Aggreg_file(models.Model):
#     document = models.FileField(upload_to=content_file_name)
# 
#     
#     def __str__(self):
#         return self.document.name
#     
#     def __unicode__(self): #For Python2, use __unicode__too
#         return str(self.document.name)
# 
#     def save(self, *args, **kwargs):
#         self.slug = self.document.name
#         super(Document, self).save(*args, **kwargs)
# 
#     
#     def delete(self, *args, **kwargs):
#         os.remove(os.path.join(settings.MEDIA_ROOT,self.document.name))
#         super(Document,self).delete(*args,**kwargs)
#==============================================================================

#==============================================================================
# @receiver(pre_delete, sender=Document)
# def document_delete(**kwargs):
#     instance = kwargs.get('instance')
#     instance.document.delete(save=False)
#  
#==============================================================================
    
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username
    
    
    
    

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)





class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'




#==============================================================================
# class LucivariCondition(models.Model):
#     id = models.IntegerField(primary_key=True)  # AutoField?
#     cond = models.CharField(max_length=128)
#     group = models.CharField(max_length=128)
#     gene = models.CharField(max_length=128)
#     cell = models.CharField(max_length=128)
#     variant = models.CharField(max_length=128)
# 
#     class Meta:
#         managed = False
#         db_table = 'lucivari_condition'
# 
# 
# class LucivariExperiment(models.Model):
#     id = models.IntegerField(primary_key=True)  # AutoField?
#     exp_id = models.CharField(unique=True, max_length=128)
#     repl = models.CharField(max_length=128)
#     date = models.DateField()
#     cond_id = models.ForeignKey(LucivariCondition, models.DO_NOTHING)
# 
#     class Meta:
#         managed = False
#         db_table = 'lucivari_experiment'
# 
#==============================================================================

class LucivariUserprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    website = models.CharField(max_length=200)
    picture = models.CharField(max_length=100)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lucivari_userprofile'


class RegistrationRegistrationprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    activation_key = models.CharField(max_length=40)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    activated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'registration_registrationprofile'


class RegistrationSupervisedregistrationprofile(models.Model):
    registrationprofile_ptr = models.OneToOneField(RegistrationRegistrationprofile, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'registration_supervisedregistrationprofile'
