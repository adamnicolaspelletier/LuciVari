# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-05-12 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('codename', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
                ('username', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Conditions',
            fields=[
                ('condition_id', models.IntegerField(blank=True, db_column='Condition_ID', primary_key=True, serialize=False)),
                ('condition_group', models.IntegerField(blank=True, db_column='Condition_Group', null=True)),
                ('cell_line', models.TextField(blank=True, db_column='Cell_line', null=True)),
                ('ff_average', models.FloatField(blank=True, db_column='FF_Average', null=True)),
                ('ff_std', models.FloatField(blank=True, db_column='FF_STD', null=True)),
                ('rn_average', models.FloatField(blank=True, db_column='RN_Average', null=True)),
                ('rn_std', models.FloatField(blank=True, db_column='RN_STD', null=True)),
                ('rlu_average', models.FloatField(blank=True, db_column='RLU_Average', null=True)),
                ('rlu_std', models.FloatField(blank=True, db_column='RLU_STD', null=True)),
                ('fc_average', models.FloatField(blank=True, db_column='FC_Average', null=True)),
                ('fc_std', models.FloatField(blank=True, db_column='FC_STD', null=True)),
            ],
            options={
                'db_table': 'conditions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
                ('action_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.TextField(blank=True, db_column='ID', primary_key=True, serialize=False)),
                ('replicate', models.TextField(blank=True, db_column='Replicate', null=True)),
                ('date', models.TextField(blank=True, db_column='Date', null=True)),
                ('experiment_number', models.IntegerField(blank=True, db_column='Experiment_number', null=True)),
                ('condition_group', models.IntegerField(blank=True, db_column='Condition_Group', null=True)),
                ('ff_value', models.FloatField(blank=True, db_column='FF_Value', null=True)),
                ('rn_value', models.FloatField(blank=True, db_column='RN_Value', null=True)),
                ('rlu_value', models.FloatField(blank=True, db_column='RLU_Value', null=True)),
                ('rlu_wt', models.FloatField(blank=True, db_column='RLU_WT', null=True)),
                ('fold_change', models.FloatField(blank=True, db_column='Fold_Change', null=True)),
            ],
            options={
                'db_table': 'experiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genes',
            fields=[
                ('gene_symbol', models.TextField(blank=True, db_column='Gene_Symbol', primary_key=True, serialize=False)),
                ('chr', models.TextField(blank=True, db_column='Chr', null=True)),
                ('gene_start_pos', models.IntegerField(blank=True, db_column='Gene_Start_Pos', null=True)),
                ('gene_stop_pos', models.IntegerField(blank=True, db_column='Gene_Stop_Pos', null=True)),
            ],
            options={
                'db_table': 'genes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LucivariUserprofile',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('website', models.CharField(max_length=200)),
                ('picture', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'lucivari_userprofile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationRegistrationprofile',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('activation_key', models.CharField(max_length=40)),
                ('activated', models.BooleanField()),
            ],
            options={
                'db_table': 'registration_registrationprofile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Snv',
            fields=[
                ('snv_id_no', models.IntegerField(blank=True, db_column='SNV_ID_NO', primary_key=True, serialize=False)),
                ('chr', models.TextField(blank=True, db_column='Chr', null=True)),
                ('variant_status', models.TextField(blank=True, db_column='Variant_status', null=True)),
                ('snv', models.TextField(blank=True, db_column='SNV', null=True)),
                ('snv_pos', models.TextField(blank=True, db_column='SNV_pos', null=True)),
                ('sift_score', models.TextField(blank=True, db_column='SIFT_SCORE', null=True)),
                ('polyphen_score', models.TextField(blank=True, db_column='Polyphen_SCORE', null=True)),
            ],
            options={
                'db_table': 'SNV',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationSupervisedregistrationprofile',
            fields=[
                ('registrationprofile_ptr', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='lucivari.RegistrationRegistrationprofile')),
            ],
            options={
                'db_table': 'registration_supervisedregistrationprofile',
                'managed': False,
            },
        ),
    ]
