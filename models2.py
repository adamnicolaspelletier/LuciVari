# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Genes(models.Model):
    gene_symbol = models.TextField(db_column='Gene_Symbol', blank=True, null=True, primary_key=True)  # Field name made lowercase.
    chr = models.TextField(db_column='Chr', blank=True, null=True)  # Field name made lowercase.
    gene_start_pos = models.IntegerField(db_column='Gene_Start_Pos', blank=True, null=True)  # Field name made lowercase.
    gene_stop_pos = models.IntegerField(db_column='Gene_Stop_Pos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'genes'

class Snv(models.Model):
    snv_id_no = models.IntegerField(db_column='SNV_ID_NO', blank=True, null=True, primary_key=True)  # Field name made lowercase.
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
        

class Conditions(models.Model):
    condition_id = models.IntegerField(db_column='Condition_ID', blank=True, null=True, primary_key=True)  # Field name made lowercase.
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
        
        
class Experiment(models.Model):
    id = models.TextField(db_column='ID', blank=True, null=True, primary_key=True)  # Field name made lowercase.
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




class LucivariCondition(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    cond = models.CharField(max_length=128)
    group = models.CharField(max_length=128)
    gene = models.CharField(max_length=128)
    cell = models.CharField(max_length=128)
    variant = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'lucivari_condition'


class LucivariExperiment(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    exp_id = models.CharField(unique=True, max_length=128)
    repl = models.CharField(max_length=128)
    date = models.DateField()
    cond_id = models.ForeignKey(LucivariCondition, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lucivari_experiment'


class LucivariUserprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    website = models.CharField(max_length=200)
    picture = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'lucivari_userprofile'


class RegistrationRegistrationprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    activation_key = models.CharField(max_length=40)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    activated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'registration_registrationprofile'


class RegistrationSupervisedregistrationprofile(models.Model):
    registrationprofile_ptr = models.ForeignKey(RegistrationRegistrationprofile, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'registration_supervisedregistrationprofile'
