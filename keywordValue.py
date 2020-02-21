
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.api as sm

#class to calculate conjoint analysis on keywords to determine a word value
class keywordValue:

    #class variables
    keyword_df = pd.DataFrame() #keywords indivdual word and score
    keyword_summary_df = pd.DataFrame() # keywords summary
    salary_df = pd.read_csv('job_avg_salaries.csv') #avg salary per job
    avg_salary = 0 #salary of a given job
    df2 = pd.DataFrame() #feature matrix holding dataframe
    feature_matrix = pd.DataFrame()   #feature matrix for conjoint analysis
    num_keywords = 50 #number of keywords
    df_final = pd.DataFrame()

    #intialize dataframe with granular and summary level keyword dataframes
    def __init__(self, keyword_df =pd.DataFrame() , keyword_summary_df=pd.DataFrame()):
        self.keyword_df = keyword_df
        self.keyword_summary_df = keyword_summary_df
        #self.keyword_df = pd.read_csv('PM_Keywords_granular.csv') #test data
        #self.keyword_summary_df = pd.read_csv('PM_Keywords_summary.csv') #test data

    def clear(self):
        self.keyword_df = pd.DataFrame()  # keywords indivdual word and score
        self.keyword_summary_df = pd.DataFrame()  # keywords summary
        self.salary_df = pd.read_csv('job_avg_salaries.csv')  # avg salary per job
        self.avg_salary = 0  # salary of a given job
        self.df2 = pd.DataFrame()  # feature matrix holding dataframe
        self.feature_matrix = pd.DataFrame()  # feature matrix for conjoint analysis
        self.num_keywords = 50  # number of keywords
        df_final = pd.DataFrame()

    #set job salary
    def setJobSalary(self, job_role):
        try:
            self.avg_salary = int(self.salary_df[self.salary_df['Job_Tittle'] == job_role].iloc[0]['Avg_Salary'])
        except: # return 0 if not found
            self.avg_salary = 0

    # filter list to the top x keywords
    def filterTopKeywords(self):
        top_keywords = self.keyword_summary_df["keyword"][:self.num_keywords].tolist()
        self.keyword_df = self.keyword_df[self.keyword_df['keyword'].isin(top_keywords)]

    #Build out feature matrix where a keyword is column (1 or 0) and a job is a row.  Add rank according to the sum of IDF keyword scores.
    def conjointDataPrep(self):

        #Build sparse matrix with each keyword as a column
        self.df2 = pd.get_dummies( self.keyword_df['keyword']).to_sparse(0)
        self.df2['job_ID'] =  self.keyword_df['job_ID']
        self.df2['Company'] =  self.keyword_df['Company']
        self.df2['Title'] = self.keyword_df['Title']
        self.df2['Score'] =  self.keyword_df['Score']

        #roll up each each keyword where a job is a row.
        self.feature_matrix = self.df2.groupby(['job_ID'], as_index=False).sum()

        #add a rank column by score
        self.feature_matrix ["Rank"] = self.feature_matrix ["Score"].rank(method='dense', ascending=False)

    def runConjoint(self):

        #build feature matrix and target variable
        Y = self.feature_matrix['Rank']
        X = self.feature_matrix[[x for x in self.feature_matrix.columns if x != 'job_ID' and x != 'Rank' and x != 'Company' and x != 'Title' and x != 'Score']]

        #run linear regression
        res = sm.OLS(Y, X, family=sm.families.Binomial()).fit()
        df_res = pd.DataFrame({ #store regression results in a dataframe
            'param_name': res.params.keys()
            , 'param_w': res.params.values
            , 'pval': res.pvalues
        })

        # adding field for absolute of parameters
        df_res['abs_param_w'] = np.abs(df_res['param_w'])
        # marking field is significant under 95% confidence interval
        df_res['is_sig_95'] = (df_res['pval'] < 0.05)
        # constructing color naming for each param
        df_res['c'] = ['blue' if x else 'red' for x in df_res['is_sig_95']]

        # make it sorted by abs of parameter value
        df_res = df_res.sort_values(by='abs_param_w', ascending=True)

        # need to assemble per attribute for every level of that attribute in dicionary
        range_per_feature = dict()
        for key, coeff in res.params.items():
            sk = key.split('_')
            feature = sk[0]
            if len(sk) == 1:
                feature = key
            if feature not in range_per_feature:
                range_per_feature[feature] = list()

            range_per_feature[feature].append(coeff)

            # importance per feature is range of coef in a feature
            # while range is simply max(x) - min(x)
        importance_per_feature = {
            k: abs(max(v)) for k, v in range_per_feature.items()
        }

        # compute relative importance per feature
        # or normalized feature importance by dividing
        # sum of importance for all features
        total_feature_importance = sum(importance_per_feature.values())
        relative_importance_per_feature = {
            k: 100 * round(v / total_feature_importance, 3) for k, v in importance_per_feature.items()
        }

        alt_data = pd.DataFrame(
            list(relative_importance_per_feature.items()),
            columns=['attr', 'relative_importance (pct)']
        ).sort_values(by='relative_importance (pct)', ascending=False)

        alt_data.rename(columns={'attr': 'keyword'}, inplace=True)
        alt_data['wordValue'] = alt_data["relative_importance (pct)"] / 100 * self.avg_salary

        self.df_final = alt_data
        print(self.df_final)
