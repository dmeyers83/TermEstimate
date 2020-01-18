

from prototypeScrapper import prototypeScrapper
from termEstimator import termEstimator
import pandas as pd
def scrape_call(searchQuery):
    scrapper_object = prototypeScrapper(searchQuery)
    print("#### page values ####")
    print(scrapper_object.page_data_list)
    print("#### json objects ####")
    termEstimator_object = termEstimator(scrapper_object.page_data_list)
    print(termEstimator_object.agg_data())
    return termEstimator_object.df

df_BLS = pd.read_csv('BLM_Computer.csv')

roles = df_BLS.OCC_TITLE.unique()
df_final = pd.DataFrame()

for job in roles:
    df_2 = pd.DataFrame()
    df_2 = scrape_call(job)
    df_2['job_name'] = job
    df_final = df_final.append(df_2)
    print("done appending")

print("print final")
df_final.to_csv('BLS_Keywords.csv')
df_final.head()