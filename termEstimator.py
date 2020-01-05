import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import re


class termEstimator:

    page_data =[] #list of documents
    term_data = []
    df = pd.DataFrame()

    def __init__(self, page_data):
        self.page_data = page_data
        self.term_data = self.extract_keywords(page_data)
        print("placeholder text")

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(self, feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""

        # use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        # results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    def get_stop_words(self, stop_file_path):
        """load stop words """

        with open(stop_file_path, 'r', encoding="utf-8") as f:
            stopwords = f.readlines()
            stop_set = set(m.strip() for m in stopwords)
            return frozenset(stop_set)

    def extract_keywords(self, page_data):
        # load a set of stop words
        stopwords = self.get_stop_words("stopwords.txt")

        # get the text column
        docs = page_data

        # create a vocabulary of words,
        # ignore words that appear in 97% of documents,
        # eliminate stop words
        cv = CountVectorizer(max_df=0.97, token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', stop_words=stopwords,
                             max_features=10000)
        word_count_vector = cv.fit_transform(docs)

        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True, sublinear_tf=True)
        # tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
        tfidf_transformer.fit(word_count_vector)

        term_list = [] # list of top terms for a given document

        for item in self.page_data:
            # you only needs to do this once, this is a mapping of index to
            feature_names = cv.get_feature_names()

            # get the document that we want to extract keywords from
            doc = item

            # generate tf-idf for the given document
            tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

            # sort the tf-idf vectors by descending order of scores
            sorted_items = self.sort_coo(tf_idf_vector.tocoo())

            # extract only the top n; n here is 10
            keywords = self.extract_topn_from_vector(feature_names, sorted_items, 10)

            # now print the results
            print("\n=====Doc=====")
            print(doc)
            print("\n===Keywords===")
            list_item = []
            for k in keywords:
                tagged = nltk.pos_tag(nltk.word_tokenize(k))
                term_list.append([k, keywords[k], str(tagged[0][1])])
                print(k, keywords[k])

        return term_list

    def agg_data(self):
        term_list= self.term_data
        self.df = pd.DataFrame(term_list, columns=["keyword", "Score", "POS"]) # Initialize Dataframe

        #map to higher level POS
        self.df['POS'] = self.df['POS'].map({'NN': 'Noun', 'NNS': 'Noun','NNP ': 'Noun Proper','NNPS': 'Noun Proper','VB': 'Verb','VBD': 'Verb','VBG': 'Verb','VBN': 'Verb','VBP': 'Verb','VBZ': 'Verb',
                          'JJ': 'Adjective','JJR': 'Adjective','JSS': 'Adjective','RB': 'Adverb','RBR': 'Adverb','RBS ': 'Adverb'})

        #split POS sections into indivual dataframes
        df_noun = self.df.loc[(self.df['POS'] == "Noun")]
        df_verb = self.df.loc[(self.df['POS'] == "Verb")]
        df_adverb = self.df.loc[(self.df['POS'] == "Adverb")]
        df_adjective = self.df.loc[(self.df['POS'] == "Adjective")]

        #df_agg_count = df.groupby(['keyword','POS'])['Score'].agg({"keyword_count": "count", "score_sum": "sum"}).sort_values(['keyword_count'],ascending=False)
        df_agg_count_noun = df_noun.groupby(['keyword'])['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'],ascending=False)[:20]
        df_agg_count_verb = df_verb.groupby(['keyword'])['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'],ascending=False)[:20]
        df_agg_count_adjective =df_adjective.groupby(['keyword'])['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'],ascending=False)[:20]
        df_agg_count_adverb = df_adverb.groupby(['keyword'])['Score'].agg({"keyword_count": "count"}).sort_values(['keyword_count'],ascending=False)[:20]

        #return json object array for each set of terms by POS
        return [df_agg_count_noun.to_json(orient='split'), df_agg_count_verb.to_json(orient='split'),df_agg_count_adjective.to_json(orient='split'), df_agg_count_adverb.to_json(orient='split') ]