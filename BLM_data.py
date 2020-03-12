

from prototypeScrapper import prototypeScrapper
from termEstimator import termEstimator
from databaseConnection import dbConnection
import pandas as pd
from keywordValue import keywordValue
from datetime import datetime

db = dbConnection() #insert in keyword collection

db2= dbConnection(collection='all_data') #insert in all data collection

def scrape_call(searchQuery,domain):
    scrapper_object = prototypeScrapper(searchQuery)
    print("#### page values ####")
    print(scrapper_object.page_data_list)
    scrapper_data_all =  scrapper_object.full_result
    scrapper_object.df_all_scraped_data['domain'] = domain
    db2.insert_df(scrapper_object.df_all_scraped_data)
    scrapper_object.df_all_scraped_data.to_csv('scrapedataall.csv')
    print("#### json objects ####")
    termEstimator_object = termEstimator(scrapper_object.df_all_scraped_data['data'].tolist(), scrapper_data_all)
    print(termEstimator_object.agg_data())
    print("#### keywords####")
    print(termEstimator_object.df.head())
    return termEstimator_object.df

#df_BLS = pd.read_csv(r"C:\Users\doug\TermEstimate\BLS_Computer.csv")

#roles = df_BLS.OCC_TITLE.unique()
#roles = ["IT Project Manager","Technology Product Manager","Data Scientist", "DevOps Engineer","Software Engineer","Data Engineer","Solutions Architect","Data Analyst","Full Stack Developer","Development Manager","CTO","CIO","Security Engineer","Mobile Application Developer","Senior Web Developer","Cloud Solutions Architect", "Information Technology Manager","Applications Architect","Big data engineer","Information systems security manager","Data security analyst"]

roles = ["Marketing Manager", "Brand Manager", "Digital Marketing Manager"]
#domain = "Information_Technology"

#roles = ["Technology Product Manager"]
domain = "Marketing"

df_granular = pd.DataFrame()
df_summary = pd.DataFrame()
df_2 = pd.DataFrame()
for job in roles:
    df_2 = df_2.iloc[0:0]
    df_2 = scrape_call(job, domain)
    df_2['query'] = job
    df_2['time'] = datetime.now()
    df_2['domain'] = domain
    df_granular = df_granular.append(df_2)
    df_2_summary = df_2.groupby(['keyword', 'POS', 'time', 'query','domain'], as_index=False)['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'], ascending=False)
    df_summary= df_summary.append(df_2_summary)

    #conjoint analysis
    conjointKeywords = keywordValue(df_2,df_2_summary) #initilize
    conjointKeywords.setJobSalary(job)
    conjointKeywords.filterTopKeywords()
    conjointKeywords.conjointDataPrep()
    conjointKeywords.runConjoint()
    df_merge_col = pd.merge(df_2_summary, conjointKeywords.df_final, on='keyword')

    data =  df_merge_col.to_dict(orient='records')  # Here's our added param..
    db.insertData(data)
    print("done appending")
    conjointKeywords.clear()

df_granular.to_csv(domain + 'Keywords_granular.csv')
df_summary.to_csv(domain + 'Keywords_summary.csv')

print("done with full script")
# print("print final")
# df_final.to_csv('IT2_Keywords_granular.csv')
# df_final.head()
#
# df_final_count = df_final.groupby(['keyword','POS','time','query'], as_index=False)['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'],ascending=False)
# #df_final_count.reset_index(level=0, inplace=True)
# print(df_final_count.head())
# df_final_count.to_csv('IT2_Keywords_summary.csv')
# data = df_final_count.to_dict(orient='records')  # Here's our added param..
# print (data)
#
#
# db.insertData(data)