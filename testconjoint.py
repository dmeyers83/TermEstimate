


from keywordValue import keywordValue
import pandas as pd

conjointKeywords = keywordValue()
conjointKeywords.setJobSalary("Technology Project Manager")
conjointKeywords.filterTopKeywords()
conjointKeywords.conjointDataPrep()
conjointKeywords.runConjoint()

keyword_summary_df = pd.read_csv('PM_Keywords_summary.csv')  # test data

df_merge_col = pd.merge(keyword_summary_df, conjointKeywords.df_final, on='keyword')
print(df_merge_col)