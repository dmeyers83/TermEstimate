# import flask library
from flask import Flask, escape, url_for, render_template, request
#from prototypeScrapper import prototypeScrapper
#from termEstimator import termEstimator
#import pickle
import json
# initialize flask app
app = Flask(__name__)
from databaseConnection import dbConnection

def save_file(object):
    with open('text_save.txt', 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(object, config_dictionary_file)

def read_file(filename):
    with open(filename, 'rb') as config_dictionary_file:
        config_dictionary = pickle.load(config_dictionary_file)
        print(config_dictionary)
        return(config_dictionary)


def scrape_call(searchQuery):
    scrapper_object = prototypeScrapper(searchQuery)
    print("#### page values ####")
    print(scrapper_object.page_data_list)
    print("#### json objects ####")
    termEstimator_object = termEstimator(scrapper_object.page_data_list)
    print(termEstimator_object.agg_data())
    save_file(termEstimator_object.agg_data())
    return (termEstimator_object.agg_data())

# Path to render the html to display the search page
@app.route('/')
def displaySearch():
    print("placeholder")
    db = dbConnection()
    query = db.returnUniqueQueryValues()
    print(query)
    return render_template('landingpage.html', searchValues=query)


# path to render the results page.  the searchQuery parameter is passed from the landing page.
@app.route('/result/<searchQuery>')
def diplayresult(searchQuery):
    print("placeholder2")
    data = scrape_call(searchQuery)
    return render_template('results.html',searchQuery=searchQuery,data=data)

# run flask app
if __name__ == '__main__':

    #print(read_file('text_save.txt'))

    app.run()

