

from prototypeScrapper import prototypeScrapper
from termEstimator import termEstimator
from databaseConnection import dbConnection
import pandas as pd
from datetime import datetime

def scrape_call(searchQuery):
    scrapper_object = prototypeScrapper(searchQuery)
    print("#### page values ####")
    print(scrapper_object.page_data_list)
    print("#### json objects ####")
    termEstimator_object = termEstimator(scrapper_object.page_data_list)
    print(termEstimator_object.agg_data())
    return termEstimator_object.df

df_BLS = pd.read_csv(r"C:\Users\doug\TermEstimate\BLS_Computer.csv")

#roles = df_BLS.OCC_TITLE.unique()
roles = ["Technology Project Manager","Technology Product Manager","Data Scientist", "DevOps Engineer","Software Engineer","Data Engineer","Solutions Architect","Data Analyst","Full Stack Developer","Development Manager","CTO","CIO","Security Engineer","Mobile Application Developer","Senior Web Developer","Cloud Solutions Architect", "Information Technology Manager","Applications Architect","Big data engineer","Information systems security manager","Data security analyst"]

df_final = pd.DataFrame()

for job in roles:
    df_2 = pd.DataFrame()
    df_2 = scrape_call(job)
    df_2['query'] = job
    df_2['time'] = datetime.now()
    df_final = df_final.append(df_2)
    print("done appending")

print("print final")
df_final.to_csv('IT_Keywords_granular.csv')
df_final.head()

df_final_count = df_final.groupby(['keyword','POS','time','query'], as_index=False)['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'],ascending=False)
#df_final_count.reset_index(level=0, inplace=True)
print(df_final_count.head())
df_final_count.to_csv('IT_Keywords_summary.csv')
data = df_final_count.to_dict(orient='records')  # Here's our added param..
print (data)
db = dbConnection()

db.insertData(data)