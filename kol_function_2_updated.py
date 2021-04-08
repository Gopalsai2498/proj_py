# -*- coding: utf-8 -*-

################### F U N C T I O N  2 ## (one record per dr and first, last, cred -- updated)


import requests
import json
import pandas as pd
import numpy as np


def de_list(input_field):
    if isinstance(input_field, list):
        if len(input_field) == 0:
            return None
        elif len(input_field) == 1:
            return input_field[0]
        else:
            return '; '.join(input_field)
    else:
        return input_field
    
extract_fields = [
    "NCTId",
    "BriefSummary",
    "BriefTitle",
    "CentralContactEMail",
    "CentralContactName",
    "CentralContactPhone",
    "CentralContactPhoneExt",
    "CentralContactRole",
    "CollaboratorClass",
    "CollaboratorName",
    "CompletionDate",
    "CompletionDateType",
    "IsFDARegulatedDevice",
    "IsFDARegulatedDrug",
    "LeadSponsorClass",
    "LeadSponsorName",
    "LimitationsAndCaveatsDescription",
    "LocationCity",
    "LocationContactEMail",
    "LocationContactName"]

extract_fields2 = [
    "NCTId",
    "LocationContactPhone",
    "LocationContactRole",
    "LocationContactPhoneExt",
    "LocationCountry",
    "LocationFacility",
    "LocationState",
    "LocationStatus",
    "LocationZip",
    "NCTIdAlias",
    "OfficialTitle",
    "OrgClass",
    "OrgFullName",
    "OrgStudyId",
    "OrgStudyIdDomain",
    "OrgStudyIdLink",
    "OrgStudyIdType",
    "OversightHasDMC",
    ]

extract_fields3 = [
    "NCTId",
    "PatientRegistry",
    "Phase",
    "PointOfContactEMail",
    "PointOfContactOrganization",
    "PointOfContactPhone",
    "PointOfContactPhoneExt",
    "PointOfContactTitle",
    "ReferencePMID",
    "ResponsiblePartyInvestigatorAffiliation",
    "ResponsiblePartyInvestigatorFullName",
    "ResponsiblePartyInvestigatorTitle"
    ]

data=pd.DataFrame()
data1=pd.DataFrame()
data2=pd.DataFrame()
minrnk = 1
maxrnk = 1000
exp = '("Vasomotor Symptoms")OR("Menopausal Symptoms")OR("Hot Flashes")OR("Hot Flushes")OR(Menopause)'
BASE_URL = 'https://clinicaltrials.gov/api/query/study_fields?expr='+str(exp)+'&min_rnk='+str(minrnk)+'&max_rnk='+str(maxrnk)+'&fmt=json'

query_url = f'{BASE_URL}&fields={",".join(extract_fields)}'
#print(query_url)

r = requests.get(query_url)
#r.status_code
# query_url = f'{BASE_URL}'
# print(query_url)
while(r.status_code == 200):
    BASE_URL = 'https://clinicaltrials.gov/api/query/study_fields?expr='+exp+'&min_rnk='+str(minrnk)+'&max_rnk='+str(maxrnk)+'&fmt=json'
    query_url = f'{BASE_URL}&fields={",".join(extract_fields)}'
    query_url2 = f'{BASE_URL}&fields={",".join(extract_fields2)}'
    query_url3 = f'{BASE_URL}&fields={",".join(extract_fields3)}'
    r = requests.get(query_url)   
    r.status_code    
    j = json.loads(r.content)
    # df = pd.DataFrame(j['FullStudiesResponse']['FullStudies'])
    df = pd.DataFrame(j['StudyFieldsResponse']['StudyFields'])   
    for c in df.columns:
        df[c] = df[c].apply(de_list)
    df['CompletionDate'] = pd.to_datetime(df['CompletionDate'])
    df = df.sort_values(by='CompletionDate', ascending=False)    
    data = data.append(df)
    
    r = requests.get(query_url2)   
    r.status_code    
    j = json.loads(r.content)
    # df = pd.DataFrame(j['FullStudiesResponse']['FullStudies'])
    df = pd.DataFrame(j['StudyFieldsResponse']['StudyFields'])   
    for c in df.columns:
        df[c] = df[c].apply(de_list)
       
    data1 = data1.append(df)
    
    r = requests.get(query_url3)   
    r.status_code    
    j = json.loads(r.content)
    # df = pd.DataFrame(j['FullStudiesResponse']['FullStudies'])
    df = pd.DataFrame(j['StudyFieldsResponse']['StudyFields'])   
    for c in df.columns:
        df[c] = df[c].apply(de_list)
     
    data2 = data2.append(df)
    
    minrnk +=1000
    maxrnk +=1000
    print(minrnk)
    if(j['StudyFieldsResponse']['NStudiesFound'] < minrnk):
        break

final_data = data.merge(data1,on='NCTId').merge(data2,on='NCTId')



###### separating into one record per dr

df = final_data.copy()

cols = df.columns.tolist()

df[['CentralContactName','CentralContactEMail', 'CentralContactPhone']] = df[['CentralContactName','CentralContactEMail', 'CentralContactPhone']].fillna('none')

df['new_name'] = df['CentralContactName'].replace(',', '', regex=True).str.split(';')
df['new_email'] = df['CentralContactEMail'].str.split(';')
df['new_phone'] = df['CentralContactPhone'].str.split(';')


cond = [(df['new_name'].str.len() == df['new_email'].str.len()) & (df['new_name'].str.len() == df['new_phone'].str.len()),
        (df['new_name'].str.len() == df['new_email'].str.len()),
        (df['new_name'].str.len() == df['new_phone'].str.len())]

val = ['all', 'name_email', 'name_ph']


df['new'] = np.select(cond, val)


df_all = df[df['new']=='all']

names = df_all['new_name'].apply(pd.Series).stack().rename('new_name').reset_index()
new_email = df_all['new_email'].apply(pd.Series).stack().rename('new_email').reset_index()
new_phone = df_all['new_phone'].apply(pd.Series).stack().rename('new_phone').reset_index()

#print(names.shape)
##print(new_email.shape)
#print(new_phone.shape)

new_phone.drop(['level_0', 'level_1'], axis=1, inplace=True)
new_email.drop(['level_0', 'level_1'], axis=1, inplace=True)

names_email_ph_all = pd.concat([names,new_email,new_phone], axis=1)

df_all_final = pd.merge(names_email_ph_all,df_all,left_on='level_0',right_index=True, suffixes=(['','_old']))[df_all.columns]


df_all_final = df_all_final.drop(['CentralContactName', 'CentralContactEMail','CentralContactPhone','new'], axis=1).rename(
    columns={'new_name':'CentralContactName', 'new_email': 'CentralContactEMail', 'new_phone':'CentralContactPhone'})

df_all_final = df_all_final[cols]



df_name_email = df[df['new']=='name_email'].drop('new_phone', axis=1)

names = df_name_email['new_name'].apply(pd.Series).stack().rename('new_name').reset_index()
new_email = df_name_email['new_email'].apply(pd.Series).stack().rename('new_email').reset_index()

#print(names.shape)
#print(new_email.shape)

new_email.drop(['level_0', 'level_1'], axis=1, inplace=True)

names_email = pd.concat([names,new_email], axis=1)

df_name_email_final = pd.merge(names_email,df_name_email,left_on='level_0',right_index=True, suffixes=(['','_old']))[df_name_email.columns]

df_name_email_final = df_name_email_final.drop(['CentralContactName', 'CentralContactEMail', 'new'], axis=1).rename(
    columns={'new_name':'CentralContactName', 'new_email': 'CentralContactEMail'})

df_name_email_final = df_name_email_final[cols]


df_name_ph = df[df['new']=='name_ph'].drop('new_email', axis=1)

names = df_name_ph['new_name'].apply(pd.Series).stack().rename('new_name').reset_index()
new_phone = df_name_ph['new_phone'].apply(pd.Series).stack().rename('new_phone').reset_index()

#print(names.shape)
#print(new_phone.shape)

new_phone.drop(['level_0', 'level_1'], axis=1, inplace=True)

names_phone = pd.concat([names,new_phone], axis=1)

df_name_ph_final = pd.merge(names_phone,df_name_ph,left_on='level_0',right_index=True, suffixes=(['','_old']))[df_name_ph.columns]

df_name_ph_final = df_name_ph_final.drop(['CentralContactName', 'CentralContactPhone', 'new'], axis=1).rename(
    columns={'new_name':'CentralContactName', 'new_phone':'CentralContactPhone'})

df_name_ph_final = df_name_ph_final[cols]


final_df_fun2 = pd.concat([df_all_final, df_name_email_final, df_name_ph_final])



#creating separate first name, last name, credentials variables from CentralContactName

df['new_name'] = df['CentralContactName'].str.replace('.', '')

names = df['new_name'].tolist()

cred = ['PhD', 'PHD', 'Associate Professor', 'Professor','Prof', 'MD', 'MSc','MS', 'BSc', 'BS', 'PI', 'DPT', 'PT', 'prof', 'MDMSCI', 'MPA', 'CCRC', 'MB', 'MSN', 'Msc', 'MPH',
        'AGPCNP-BC ACHPN', 'JD', 'RDN', 'Dr','FRCSC', 'RN', 'AP', 'DDS', 'FAAD', 'CRC' 'N', 'doctor', 'BBMED',  'BChMRCP', 'PharmD', 'B Sc', 'DO', 'FRCP', 'MA', 'Pr']

clean_names = []
first_name = []
middle_name = []
last_name = []
title = []

for name in names:
    to_remove = cred
    clean_name = name
    for element in to_remove:
        clean_name = clean_name.replace(element,'')
    clean_names.append(clean_name)

for (name, orig_name) in zip(clean_names, names):
    data = name.split()
    #print(len(data) <2, data)
    
    if len(data) <2:
        first_name.append("")
        middle_name.append("")
        last_name.append("")
        title.append("")
        continue
    
    first_name.append(data[0])
    
    if len(data) == 2:
        middle_name.append("")
        last_name.append(data[1])
        
    else:
        middle_name.append(data[1])
        last_name.append(" ".join(data[2:]))
    
    title.append(' ,'.join([suf for suf in cred if suf in orig_name]))

df['first_name'] = first_name
df['middle_name'] = middle_name
df['last_name'] = last_name
df['credential'] = title

df_last_first_cred_df = df.copy()

