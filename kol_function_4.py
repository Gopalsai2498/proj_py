# -*- coding: utf-8 -*-


################### F U N C T I O N  4 ##

import pandas as pd
import requests

#https://download.cms.gov/nppes/NPI_Files.html
#https://npiregistry.cms.hhs.gov/registry/API-Examples

#parameters
#https://npiregistry.cms.hhs.gov/registry/help-api

header = {    
    #NPI-1 or NPI-2
    'enumeration_type': 'NPI-1',   
    
    #2.0 or 2.1
    'version':'2.0',               

    #city of provider's address identified in Address Purpose
    'city':'Rockville',
    
    #state abbr. of provider's address identified in Address Purpose
    'state':'MD',
    }

basic_col =['ein', 'organization_name', 'last_name', 'first_name', 'middle_name', 'name_prefix', 'name_suffix', 'credential',
            'last_updated', 'deactivation_reason_code', 'deactivation_date', 'reactivation_date', 'gender',
            'authorized_official_telephone_number']

address_col = ['address_1', 'address_2', 'city', 'state', 'postal_code', 'country_code', 'telephone_number']

taxo_col = ['license', 'state']

df = pd.DataFrame([])

r = requests.get('https://npiregistry.cms.hhs.gov/api/?'+str('skip=')+'&'+str('enumeration_type=')+str(header['enumeration_type'])+'&'+
                 str('version=')+str(header['version'])+'&'+str('city=')+str(header['city'])+'&'+str('state='+str(header['state']))+'&'+
                 str('limit=')+str('200'))

data=r.json()
d = pd.DataFrame.from_dict(data['results'])

df = df.append(d)
print(r.url)

#i=200

#while (r.status_code==200):
for i in list(range(200, 1000, 200)):

    r = requests.get('https://npiregistry.cms.hhs.gov/api/?'+str('skip=')+str(i)+'&'+str('enumeration_type=')+str(header['enumeration_type'])+'&'+
                 str('version=')+str(header['version'])+'&'+str('city=')+str(header['city'])+'&'+str('state=')+'&'+
                 str('limit=')+str('200'))
    
    data=r.json()
    d = pd.DataFrame.from_dict(data['results'])
    
    df = df.append(d)
    
    #i=i+200
    print(r.url)
    

d = df[['number', 'basic', 'addresses', 'taxonomies']]

#fetch attributes from basic
basic = d.basic.apply(pd.Series)
basic_df = pd.DataFrame(columns=basic_col)
basic_df = pd.concat([basic_df,basic]).fillna('none')
basic_df = basic_df[basic_col]

d = pd.concat([d,basic_df], axis=1)

#fetch attributes from address
d = d.explode('addresses')
addresses = d.addresses.apply(pd.Series)

address_df = pd.DataFrame(columns=address_col)
address_df = pd.concat([address_df,addresses]).fillna('none')
address_df = address_df[address_col]
address_df = address_df.rename(columns={'state':'address_state'})

d = pd.concat([d,address_df], axis=1)

#fetch attributes from taxonomies
d = d.explode('taxonomies')
taxonomies = d.taxonomies.apply(pd.Series)

taxo_df = pd.DataFrame(columns=taxo_col)
taxo_df = pd.concat([taxo_df,taxonomies]).fillna('none')
taxo_df = taxo_df[taxo_col]
taxo_df = taxo_df.rename(columns={'state':'taxo_state'})

d = pd.concat([d,taxo_df], axis=1) 
d = d.drop(['basic', 'addresses','taxonomies'], axis=1)
d = d.drop_duplicates()

#rename columns
d = d.rename(
columns={'number':'NPI', 'ein': 'Employer_Identification_Number_(EIN)', 'organization_name':'Provider_Organization_Name_(Legal_Business_Name)',
         'last_name':'Provider_Last_Name_(Legal_Name)', 'first_name': 'Provider_First_Name', 'middle_name':'Provider_Middle_Name',
         'name_prefix': 'Provider_Name_Prefix_Text', 'name_suffix': 'Provider_Name_Suffix_Text',
         'credential': 'Provider_Credential_Text', 'last_updated': 'Last_Update_Date',
         'deactivation_reason_code':'NPI_Deactivation_Reason_Code', 'deactivation_date': 'NPI_Deactivation_Date',
         'reactivation_date': 'NPI_Reactivation_Date', 'gender':'Provider_Gender_Code',
         'authorized_official_telephone_number':'Authorized_Official_Telephone_Number',
         'address_1': 'Provider_First_Line_Business_Mailing_Address', 'address_2': 'Provider_Second_Line_Business_Mailing_Address',
         'city': 'Provider_Business_Mailing_Address_City_Name',
         'address_state': 'Provider_Business_Mailing_Address_State_Name',
         'postal_code' : 'Provider_Business_Mailing_Address_Postal_Code', 'country_code' : 'Provider_Business_Mailing_Address_Country_Code_(If_outside_US)',
         'telephone_number': 'Provider_Business_Mailing_Address_Telephone_Number', 'license': 'Provider_License_Number_1',
         'taxo_state':'Provider_License_Number_State_Code_1'})

final_df = d.copy()

final_df.to_csv('d:/kol/csv/func4.csv')

final_df.columns.tolist()



final_df.columns.tolist()