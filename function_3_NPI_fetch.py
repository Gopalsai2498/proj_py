# -*- coding: utf-8 -*-


#fetching NPIs for function 3

import pandas as pd
import requests

df = func_3_df.copy()

#cleaning zip codes
df['recipient_zip_code'].str.replace(r'\D+','')

df['list'] = df.apply(lambda x: (x['physician_first_name'], x['physician_last_name'], x['recipient_city'], x['recipient_state'],
                                 x['recipient_zip_code']), axis=1)

df_new = pd.DataFrame([])

for x in df['list'].tolist():
    r = requests.get('https://npiregistry.cms.hhs.gov/api/?'+
                     str('enumeration_type=NPI-1')+'&'+
                     str('version=2.1')+'&'+ #+str(x['version'])+'&'+
                     str('first_name=')+str(x[0])+'&'+
                     str('last_name=')+str(x[1])+'&'+
                     str('state=')+str(x[3])+'&'+
                     str('postal_code=')+str(x[4])+'&'+
                     str('skip=')+str('')+'&'+str('limit=')+str(''))
    data=r.json()
    d = pd.DataFrame.from_dict(data['results'])
    
    #exclude zip code
    if not d.empty:
        df_new = df_new.append(d)
        print(r.url)
    else:
        r = requests.get('https://npiregistry.cms.hhs.gov/api/?'+
                         str('enumeration_type=NPI-1')+'&'+
                         str('version=2.1')+'&'+ #+str(x['version'])+'&'+
                         str('first_name=')+str(x[0])+'&'+
                         str('last_name=')+str(x[1])+'&'+
                         str('state=')+str(x[3])+'&'+
                         #str('postal_code=')+str(x[4])+'&'+
                         str('skip=')+str('')+'&'+str('limit=')+str(''))
        data=r.json()
        d = pd.DataFrame.from_dict(data['results'])
        
        #exclude zip code & state
        if not d.empty:
            df_new = df_new.append(d)
            print('excluded zip ' + r.url)

        else:
            r = requests.get('https://npiregistry.cms.hhs.gov/api/?'+
                             str('enumeration_type=NPI-1')+'&'+
                             str('version=2.1')+'&'+ #+str(x['version'])+'&'+
                             str('first_name=')+str(x[0])+'&'+
                             str('last_name=')+str(x[1])+'&'+
                             #str('state=')+str(x[3])+'&'+
                             #str('postal_code=')+str(x[4])+'&'+
                             str('skip=')+str('')+'&'+str('limit=')+str(''))
            data=r.json()
            d = pd.DataFrame.from_dict(data['results'])

            df_new = df_new.append(d)
            print('excluded state & zip ' + r.url)


basic_col =['ein', 'organization_name', 'last_name', 'first_name', 'middle_name', 'name_prefix', 'name_suffix', 'credential',
            'last_updated', 'deactivation_reason_code', 'deactivation_date', 'reactivation_date', 'gender',
            'authorized_official_telephone_number']

address_col = ['address_1', 'address_2', 'city', 'state', 'postal_code', 'country_code', 'telephone_number']

taxo_col = ['license', 'state']

d = df_new[['number', 'basic', 'addresses', 'taxonomies']]

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

func_3_npi_df = d.drop_duplicates('NPI', keep='first')

func_3_npi_df.head()

