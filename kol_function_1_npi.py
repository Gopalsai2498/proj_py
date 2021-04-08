# -*- coding: utf-8 -*-


import pandas as pd
import re

func_1_df = func_1_df.copy()

name_list = func_1_df['address'].tolist()


my_dic = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

country=[]
state=[]
for names in name_list:
    asplit = names.split(',')
    lis = len(asplit)
    country.append(' '.join(asplit[lis-1].split()))
    state.append(' '.join(asplit[lis-2].split()))
    
    regex = re.compile(r'\D+')
    state = [regex.search(i).group() for i in state]
    state = [x.strip(' ') for x in state]
    
    for key, val in my_dic.items():
        for i, v in enumerate(country):
            #print(v, key)
            if v == key:
                country[i] = val
    
    for key, val in my_dic.items():
        for i, v in enumerate(state):
            #print(v, key)
            if v == key:
                state[i] = val
            
    regex = re.compile('USA|USA \w*|United \w*')
    
    new_country=[]
    #new_country1=[]
    for i, x in enumerate(country):
        if regex.match(x):
            new_country.append(state[i])

        else:
            new_country.append(country[i])

func_1_df['state'] = new_country

#remove middle name from the first name
sp = func_1_df['firstname'].str.split(' ')

firstname_new = []
for x in sp.tolist():
    firstname_new.append(x[0])
    
func_1_df['new_firstname'] = firstname_new

   
#filter records
df = func_1_df[func_1_df['state'].isin(my_dic)]
