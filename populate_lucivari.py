#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 09:52:57 2017

@author: adamnicolaspelletier
"""
import sqlite3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

# import django
# django.setup()
# from lucivari.models import Condition, Experiment
import pandas as pd
import itertools
import random
import numpy as np
import datetime as dt

# def populate():
    
    
 
    # for cat, cat_data in cats.items():
    #     c = add_cat(cat,cat_data["views"],cat_data["likes"])
    #     for p in cat_data["pages"]:
    #         add_page(c, p["title"], p["url"], p["views"])
     
    #  # Print out the categories we have added.
    # for c in Category.objects.all():
    #     for p in Page.objects.filter(category=c):
    #         print("- {0} - {1}".format(str(c), str(p)))
    
 
    

 




testgenelist = []
for i in range(10):
    testgenelist.append("TF"+str(i+1))

snvlist = ["WT", "SNV1","SNV2","SNV3","SNV4","SNV5","SNV6"]

family = ["ETS", "bHlH", "bZIP", "HMG"]


celllines = ["COS-7", "293T", "HeLa", "THP-1", "MonoMac1", "Kg1a", "SCC-3", "NOMO-1", "Kasumi-1", "OP-1"]

genelist = []
repl = ["repl1","repl2","repl3"]
for i in testgenelist:
    genelist.append( i + ", Chr" + str(random.randrange(1,22)))
    

a = [genelist,snvlist]
b = list(itertools.product(*a))
cint= []
c = []

for i in b:
    cint.append(list(i))


for i in cint: 
    a = i[0].split(", ")
    i[0] = a
    i[1] = [i[1]]
    
for i in cint:
     c.append([item for sublist in i for item in sublist])


for i in c:
    i.append("rs" +str(random.randrange(100,9999999)))
    i.append(str(random.randrange(0,100000000)))
    i.append(str(random.choice([-1] * 20 + [1] *80)))

e = []
for i in c:    
    e.append(','.join(i))

f = [e, celllines, repl]
g = list(itertools.product(*f))


h = []
for i in g:
    h.append(list(i))


ID = 1
for i in h:
    i.append((str(ID)))
    ID += 1

for i in h:
    a = i[0].split(",")
    i[0] = a
    i[1] = [i[1]] 
    i[2] = [i[2]] 
    i[3] = [i[3]]

final =[]
for i in h:
    final.append([item for sublist in i for item in sublist])

tfdf = pd.DataFrame(final)

pd.options.mode.chained_assignment = None  # default='warn
cols = ["Gene_Symbol", "Chr","Variant_status","SNV", "SNV_pos", "Act_repr", "Cell_line", "Replicate", "ID"]

tfdf.columns = cols

genelist = list(tfdf["Gene_Symbol"].unique())

genestartdict = {}
genestopdict = {}

for i in genelist:
    start = random.randrange(0,100000000)
    stop = start + random.randrange(5000,20000)
    genestartdict[i] = start
    genestopdict[i] = stop

tfdf["Gene_Start_Pos"] = tfdf["Gene_Symbol"].map(genestartdict)
tfdf["Gene_Stop_Pos"] = tfdf["Gene_Symbol"].map(genestopdict)


snvlist = list(tfdf["SNV"].unique())

groupdf = tfdf[["SNV","SNV_pos", "Gene_Start_Pos", "Gene_Stop_Pos"]]
groupdf = groupdf.drop_duplicates()
groupdf["length"] = groupdf["Gene_Stop_Pos"] - groupdf["Gene_Start_Pos"]
groupdf["random"] = np.random.choice(range(1,5000),groupdf.shape[0])
groupdf["SNV_pos"] = groupdf["random"] + groupdf["Gene_Start_Pos"]
# groupdf["random"] = np.random.choice()
snvpostdict = groupdf.set_index("SNV")["SNV_pos"].to_dict()



tfdf["SNV_pos"]= tfdf["SNV"].map(snvpostdict)



tfdf.loc[tfdf["Variant_status"]=="WT", ["SNV"]] = "WT"
tfdf.loc[tfdf["Variant_status"]=="WT", ["SNV_pos"]] = "-"



df = tfdf[["Gene_Symbol","Replicate","Cell_line","Variant_status", "ID", "Act_repr"]]
catgroups = ["Gene_Symbol","Replicate","Cell_line"]


grouped = df.groupby(catgroups)

resultsdict = {}
groupdict = {}
groupfinaldict = {}

for name, group in grouped:
    
    test = pd.DataFrame(list(group.index.values))
    test = test.set_index(0)
    test["group"]= [name] *len(group)
    
    resultsdicttemp = test["group"].to_dict()
    resultsdict.update(resultsdicttemp)


grouplist = []
groupno = 1
for i in resultsdict:
    if resultsdict[i] not in grouplist:
        grouplist.append(resultsdict[i])
        groupdict[resultsdict[i]] = groupno
        groupno += 1

for i in resultsdict:
    groupfinaldict[i] = groupdict[resultsdict[i]]

df["group"]= df.index.to_series().map(groupfinaldict)







#FIRST TABLE
expdf = df[["ID","group","Gene_Symbol", "Cell_line", "Variant_status","Replicate"]]
expdatesdict = {}
experimentnodict = {}
expno = 1
for i in list(expdf["group"].unique()):
    year = 2017
    month = random.randint(1,11)
    day = random.randint(1,27)
    expdatesdict[i] = str(dt.date(year,month,day))
    experimentnodict[i] = expno 
    expno +=1

expdf["Date"] = expdf["group"].map(expdatesdict)
expdf["Experiment_number"] = expdf["group"].map(experimentnodict)


expdf["hack"] = expdf["Gene_Symbol"] +"_" +  expdf["Cell_line"] + "_" + expdf["Variant_status"]


conditioniddict = {}
condno = 1

for i in list(expdf["hack"].unique()):
    conditioniddict[i] = condno
    condno += 1

expdf["Condition_ID"] = expdf["hack"].map(conditioniddict)
del expdf["hack"]
expdf["hack"] = expdf["Gene_Symbol"] +"_" +  expdf["Cell_line"]

conditiongroupdict = {}
condno = 1

for i in list(expdf["hack"].unique()):
    conditiongroupdict[i] = condno
    condno += 1
expdf["Condition_Group"] = expdf["hack"].map(conditiongroupdict)
del expdf["hack"]


## NEED A TABLE FOR LUCIFERASE SUMMARY: GROUP, Experiement_number_list[],GENE, SNV, MEAN_FC, MEAN_STD, MEAN_RLU, MEAN_RLU_STD,
summdf = expdf[["Condition_ID", "Condition_Group", "Gene_Symbol", "Cell_line", "Variant_status" ]].drop_duplicates()



actrepr = {}
for i in list(summdf["Gene_Symbol"].unique()):
    actrepr[i] = random.choice([-1] * 20 + [1] *80)

actrepgroup = {} 
for i in list(summdf["Condition_Group"].unique()):
    actrepgroup[i] = random.choice([-1] * 80 + [1] *20)

summdf["Act_repr"] = summdf["Gene_Symbol"].map(actrepr)
summdf["Group_Act_repr"] = summdf["Condition_Group"].map(actrepgroup)

rnbasedict = {}
ffbasedict = {}

for i in list(summdf["Cell_line"].unique()):
    transfcoeff = random.randint(2000,20000)
    ffbasedict[i] = transfcoeff
    rnbasedict[i] = transfcoeff *13

summdf["FF_BASE"] = summdf["Cell_line"].map(ffbasedict)
summdf["RN_BASE"] = summdf["Cell_line"].map(rnbasedict)




condgroupwtff = {}
condgroupwtrn = {}
condgroupid = {}

for index, row in summdf.iterrows():
    if row["Variant_status"] == "WT":
        condgroupwtff[row["Condition_Group"]] = row["FF_BASE"] * float(random.randint(10,20))/10
        condgroupwtrn[row["Condition_Group"]] = row["RN_BASE"] * float(random.randint(10,20))/10
        condgroupid[row["Condition_ID"]] = row["Condition_Group"]
    


summdf["FF_WT"] = summdf["Condition_Group"].map(condgroupwtff)

damaging = random.sample(range(120,500),80)
nondamaging = random.sample(range(100,120),20)
damaging[:] = [float(x) / 100 for x in damaging]
nondamaging[:] = [float(x) / 100 for x in nondamaging]

ffsnvsdict = {}
rnsnvsdict = {}



for index, row in summdf.iterrows():
    if row["Variant_status"] != "WT":
        ffsnvsdict[row["Condition_ID"]] = row["FF_WT"] * (random.choice(damaging+nondamaging) ** float(row["Group_Act_repr"]))
        rnsnvsdict[row["Condition_ID"]] = row["RN_BASE"]
    else:
        ffsnvsdict[row["Condition_ID"]] = row["FF_WT"]
        rnsnvsdict[row["Condition_ID"]] = row["RN_BASE"]






expdf["FF_Average"] = expdf["Condition_ID"].map(ffsnvsdict)
expdf["RN_Average"] = expdf["Condition_ID"].map(rnsnvsdict)




expdf["FF_Value"] = expdf["FF_Average"] * np.random.uniform(0.95, 1.05, size=len(expdf))
expdf["RN_Value"] = expdf["RN_Average"] * np.random.uniform(0.95, 1.05, size=len(expdf))

del expdf["FF_Average"]
del expdf["RN_Average"]

expdf["FF_Average"] = expdf["FF_Value"].groupby(expdf["Condition_ID"]).transform('mean')
expdf["FF_STD"] = expdf["FF_Value"].groupby(expdf["Condition_ID"]).transform('std')
expdf["RN_Average"] = expdf["RN_Value"].groupby(expdf["Condition_ID"]).transform('mean')
expdf["RN_STD"] = expdf["RN_Value"].groupby(expdf["Condition_ID"]).transform('std')

expdf["RLU_Value"] = expdf["FF_Value"] / expdf["RN_Value"]
expdf["RLU_Average"] = expdf["RLU_Value"].groupby(expdf["Condition_ID"]).transform('mean')
expdf["RLU_STD"] = expdf["RLU_Value"].groupby(expdf["Condition_ID"]).transform('std')


rluwtdict = {}
for index, row in expdf.iterrows():
    if row["Variant_status"] == "WT":
        rluwtdict[row["Condition_Group"]] = row["RLU_Average"]
expdf["RLU_WT"] = expdf["Condition_Group"].map(rluwtdict)
expdf["Fold_Change"] = expdf["RLU_Value"]/expdf["RLU_WT"]
expdf["FC_Average"] = expdf["Fold_Change"].groupby(expdf["Condition_ID"]).transform('mean')
expdf["FC_STD"] = expdf["Fold_Change"].groupby(expdf["Condition_ID"]).transform('std')

transdf = expdf[["Condition_ID", "FF_Average", "FF_STD", "RN_Average", "RN_STD", "RLU_Average", "RLU_STD", "FC_Average", "FC_STD"]].drop_duplicates()

del summdf["FF_BASE"]
del summdf["RN_BASE"]
del summdf["FF_WT"]
del summdf["Act_repr"]
del summdf["Group_Act_repr"]

summdf = summdf.merge(transdf)

del expdf["RN_Average"]
del expdf["FF_Average"]
del expdf["RN_STD"]
del expdf["FF_STD"]
del expdf["RLU_Average"]
del expdf["RLU_STD"]
del expdf["FC_Average"]
del expdf["FC_STD"]
del expdf["Cell_line"]
del expdf["group"]
expdf = expdf.set_index('ID')
#### NEED A TABLE OF EXPERIMENTS : Experiment number, CONDITION NUMBER (ID),GROUP , DATE, GENE, , CELL-LINE, APPROVAL(Y/N), RLU, RLU_STD, REPLICATE#, FOLD_CHANGE, FC_STD, FF_AVERAGE, FF_STD, RN_AVERAGE, RN_STD

genodf = tfdf[["Gene_Symbol","Chr", "Gene_Start_Pos", "Gene_Stop_Pos"]].drop_duplicates()


#### NEED A TABLE FOR VARIANTS. POS, NAME, CHANGE, SIFT SCORE, POLYPHEN SCORE,

snvdf = tfdf[["Gene_Symbol", "Chr", "Variant_status", "SNV", "SNV_pos" ]].drop_duplicates()

#NEED A TABLEFOR GENOMIC INFO: GENESTART AND STOP, CHR, SYMBOL, 


sift = []
polyphen = []


for index, row in snvdf.iterrows():
    if row["Variant_status"] != "WT":
        sift.append(str(float(random.randint(0,10))/100))
        polyphen.append(str(float(random.randint(90,100))/100))
    else:
        sift.append("-")
        polyphen.append("-")

snvdf["SIFT_SCORE"] = sift
snvdf["Polyphen_SCORE"] = polyphen





############## Clean up tables to reduce redundancy and have unique values  that map to other tables..

snvdf["hack"] = snvdf["Gene_Symbol"] +"_" +  snvdf["Variant_status"]
snviddict = {}
snvno = 1
for i in list(snvdf["hack"].unique()):
    snviddict[i] = snvno
    snvno += 1
snvdf["SNV_ID_NO"] = snvdf["hack"].map(snviddict)
del snvdf["hack"]


summdf["hack"] = summdf["Gene_Symbol"] +"_" +  summdf["Variant_status"]
snviddict = {}
snvno = 1
for i in list(summdf["hack"].unique()):
    snviddict[i] = snvno
    snvno += 1
summdf["SNV_ID_NO"] = summdf["hack"].map(snviddict)
del summdf["hack"]
del summdf["Variant_status"]


expdf["hack"] = expdf["Gene_Symbol"] +"_" +  expdf["Variant_status"]
snviddict = {}
snvno = 1
for i in list(expdf["hack"].unique()):
    snviddict[i] = snvno
    snvno += 1
expdf["SNV_ID_NO"] = expdf["hack"].map(snviddict)

del expdf["hack"]
del expdf["Variant_status"]





snvdf = snvdf.set_index("SNV_ID_NO")
summdf = summdf.set_index('Condition_ID')

genodf = genodf.set_index('Gene_Symbol')


### Template Files
template_files = [("Template_Lucif_Assay", "template_luciferase.txt"), ("Template_Multi-Read_Raw" , "template-multi-read.txt")]
labels = ["Description", "filename"]
template_file_df = pd.DataFrame.from_records(template_files, columns=labels)

### Generic Upload File naming
generic_files = [("Lucif_Assay_Report", "lucif_raw_file.txt"), ("Consol_FF" , "consol_ff.txt"), ("Consol_RN" , "consol_rn.txt")]
labels = ["Description", "filename"]
generic_file_df = pd.DataFrame.from_records(generic_files, columns=labels)



#Export to DATABASE SECTION

conn = sqlite3.connect("db.sqlite3")

expdf.to_sql("experiment", conn, if_exists = "replace")
summdf.to_sql("conditions", conn, if_exists = "replace")
snvdf.to_sql("SNV", conn, if_exists = "replace")
genodf.to_sql("genes", conn, if_exists = "replace")
template_file_df.to_sql("templates", conn, if_exists = "replace")
generic_file_df.to_sql("generic", conn, if_exists = "replace")

# print pd.read_sql_query("select * from test;", conn)

