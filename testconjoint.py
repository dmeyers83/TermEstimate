


import pandas as pd

roles = ["IT Project Manager","Technology Product Manager","Data Scientist", "DevOps Engineer","Software Engineer","Data Engineer","Solutions Architect","Data Analyst","Full Stack Developer","Development Manager","CTO","CIO","Security Engineer","Mobile Application Developer","Senior Web Developer","Cloud Solutions Architect", "Information Technology Manager","Applications Architect","Big data engineer","Information systems security manager","Data security analyst"]

salary_df = pd.read_csv('job_avg_salaries.csv') #avg salary per job
salary_df_list = salary_df['Job_Tittle'].to_list()

for job in roles:
    if job in salary_df_list:
        print("yes " +job)
    else:
        print("no " + job)