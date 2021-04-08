# -*- coding: utf-8 -*-

import pandas as pd
from Bio import Entrez
import re

query = '(vasomotor symptoms[TIAB] | menopausal symptom[TIAB] | hot flashes[TIAB] | hot flushes[TIAB]) & "2019"[DP]'

Entrez.email = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
handle = Entrez.esearch(db='pubmed', 
                        sort='relevance', 
                        retmax='500',
                        retmode='xml', 
                        term=query)
result = Entrez.read(handle)

id_list = result['IdList']

ids = ','.join(id_list)
Entrez.email = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
handle = Entrez.efetch(db='pubmed',
                       retmode='xml',
                       id=ids)
results = Entrez.read(handle)


#first name, last name, email
def get_first_last_email(json_name):    
    firstname =[]
    lastname=[]
    email=[]
    
    for author in json_name:
        
        #email
        try:
            firstname.append(author['ForeName'])
            lastname.append(author['LastName'])
            
            #len(results['PubmedArticle'][12]['MedlineCitation']['Article']['AuthorList'][0]['AffiliationInfo'])
            s = author['AffiliationInfo'][0]['Affiliation']
            email_list = re.findall('\S+@\S+', s)
            if len(email_list)>0:
                #email = ''.join(email_list)
                t_email = ''.join(email_list)
                email.append(t_email)
            else:
                email.append('none')
        except IndexError:
            email.append('none')
        
        except KeyError:
            firstname.append('none')
            lastname.append('none')

    return firstname, lastname, email


#keyword:
def get_keywords(json_key):
    len_keyList = len(json_key)
    keyword = []
    
    if len_keyList > 0:
        for key in json_key[0]:
            keyword.append(key)
        keyword='; '.join(keyword)
    else:
        keyword ='none'
    return keyword


rows = []

for i, key in enumerate(id_list):
    temp=[]
    temp2=[]
    
    try:
        title = results['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleTitle']  
        jabbrv = results['PubmedArticle'][i]['MedlineCitation']['Article']['Journal']['ISOAbbreviation']
        journal = results['PubmedArticle'][i]['MedlineCitation']['Article']['Journal']['Title']
        pmid = results['PubmedArticle'][i]['MedlineCitation']['PMID'][0:]
        abstract = results['PubmedArticle'][i]['MedlineCitation']['Article']['Abstract']['AbstractText'][0][0:]
        year = results['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleDate'][0]['Year']
        month = results['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleDate'][0]['Month']
        day = results['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleDate'][0]['Day']
        doi = results['PubmedArticle'][i]['MedlineCitation']['Article']['ELocationID'][0][0:]
        add = results['PubmedArticle'][i]['MedlineCitation']['Article']['AuthorList'][0]['AffiliationInfo'][0]['Affiliation']
        address = re.sub('\..*','',add)
        
        keywords = get_keywords(results['PubmedArticle'][i]['MedlineCitation']['KeywordList'])
        
        firstname, lastname, email = get_first_last_email(results['PubmedArticle'][i]['MedlineCitation']['Article']['AuthorList'][0:])
    
    except KeyError:
        abstract = 'none'
        keywords='none'
        
        
    except IndexError:
        title = 'none'
        jabbrv ='none'
        journal = 'none'
        pmid ='none'
        year = 'none'
        month= 'none'
        day= 'none'
        doi='none'
        address='none'
        firstname, lastname, email = 'none', 'none', 'none'
    
    temp.extend((pmid,doi,title, abstract, year, month, day, jabbrv, journal,keywords))
    
    temp2.extend((pmid,doi,title, abstract, year, month, day, jabbrv, journal,keywords, lastname, firstname, address, email))
    
    #firstname, lastname, email = get_first_last_email(results['PubmedArticle'][i]['MedlineCitation']['Article']['AuthorList'][0:])
    if not lastname=='none':
        for last, first, em in zip(lastname, firstname, email):
            temp1=temp.copy()
            temp1.extend((last, first, address, em))
            #temp1.append(temp)
            rows.append(temp1)
    else:
        #temp1=temp.copy()
        rows.append(temp2)
        
    pubmed_df =pd.DataFrame(rows, columns=['pmid', 'doi', 'title', 'abstract', 'year', 'month', 'day','jabbrv', 'journal',
                                           'keywords', 'lastname', 'firstname', 'address', 'email'])
    

pubmed_df.to_csv('d:/kol/npi/func1_df.csv', index=False)