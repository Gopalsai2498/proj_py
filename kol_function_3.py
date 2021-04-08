# -*- coding: utf-8 -*-


################### F U N C T I O N  3 ##

import pandas as pd
from sodapy import Socrata
#https://openpaymentsdata-origin.cms.gov/browse

client = Socrata("openpaymentsdata.cms.gov", None)

#fetch dataset_ids - ap6w-xznw
results = client.get("ap6w-xznw")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#general payment dataset_id list
general_ids = results_df[results_df['dataset_name'].str.contains('General Payment')]['dataset_id'].to_list()

#research payment dataset_id list
research_ids = results_df[results_df['dataset_name'].str.contains('Research Payment')]['dataset_id'].to_list()

#ownership payment dataset_id list
ownership_ids = results_df[results_df['dataset_name'].str.contains('Ownership')]['dataset_id'].to_list()


########################
#fetch general payments
general_payments_df = pd.DataFrame([])

client = Socrata("openpaymentsdata.cms.gov", None)

for i in general_ids:
    results = client.get_all(str(i))
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    general_payments_df = general_payments_df.append(results_df)
    

general_payments_df.to_csv('d:/kol/function_3_general_payments.csv')


########################
#fetch research payments
research_payments_df = pd.DataFrame([])

client = Socrata("openpaymentsdata.cms.gov", None)

for i in research_ids:
    #results = client.get_all(str(i))
    results = client.get(str(i), limit=500)
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    research_payments_df = research_payments_df.append(results_df)
    

research_payments_df.to_csv('d:/kol/function_3_research_payments.csv')


########################
#fetch ownership payments
ownership_payments_df = pd.DataFrame([])

client = Socrata("openpaymentsdata.cms.gov", None)

for i in ownership_ids:
    #results = client.get_all(str(i))
    results = client.get(str(i), limit=500)
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    ownership_payments_df = ownership_payments_df.append(results_df)
    
ownership_payments_df.to_csv('d:/kol/function_3_ownership_payments.csv')