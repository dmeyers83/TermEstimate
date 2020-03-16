# import flask library
from flask import Flask, escape, url_for, render_template, request
#from prototypeScrapper import prototypeScrapper
#from termEstimator import termEstimator
#import pickle
import json
# initialize flask app
app = Flask(__name__)
from databaseConnection import dbConnection
import random
db = dbConnection() #keyword

db2 = dbConnection(collection='directory')



#https://visjs.github.io/vis-network/examples/static/jsfiddle.1e459ff7d7345694e4e5563fcf087a54980b2d41e612c02f7f5133da1c4da9f5.html
def buildGraph(keywords):
    #get 15 keywords
    keywords_trim = keywords[:7]
    graph = {}

    for word in keywords_trim:
        returnQuery = db.returnQueryValues(word['keyword'],3)
        print("return query start")
        print(returnQuery)
        for object in returnQuery:
            if object['query'] in graph:
                graph[object['query']].append(object['keyword'])
            else:
                graph[object['query']] = [object['keyword']]

    print(graph)

    # #Build Node List
    # nodes = []
    # edge_data = []
    # count = 1
    # for key,value in graph.items():
    #     nodes.append({'id': count, 'label': key})
    #     edge_data.append(value)
    #     count +=1
    #
    # print ("print nodes")
    # print (nodes)
    #
    #
    # #Build Edge List
    # edges = []
    # for i in range(len(edge_data)):
    #     for j in range(len(edge_data[i])):
    #         for k in range(i, len(edge_data)):
    #             if edge_data[i][j] in edge_data[k] and i!=k:
    #                 edges.append({'from': i+1, 'to': k+1, 'label':edge_data[i][j]})

    #Build Node List
    nodes = []
    edge_data = []
    count = 1
    for key,value in graph.items():
        nodes.append( {'id': str(count), 'label':key,'x':random.uniform(0, 1), 'y':random.uniform(0, 1), 'size':50, 'color': '#969696' })
        edge_data.append(value)
        count +=1

    print ("print nodes")
    print (nodes)


    #Build Edge List
    edges = []
    countEdges = {}
    for i in range(len(edge_data)): # loop t
        for j in range(len(edge_data[i])):
            for k in range(i, len(edge_data)):
                if edge_data[i][j] in edge_data[k] and i!=k:
                    key = str(i+1) + "_" + str(k+1)
                    if key in countEdges:
                        countEdges[key] +=1
                    else:
                        countEdges[key] =0
                    edges.append({'id': str(i+1) + "_" + str(k+1)+ "_" + str(j+1),'label': edge_data[i][j], 'source': str(i+1), 'target': str(k+1), 'type': 'curvedArrow','count':countEdges[key]*20, 'size':10, 'color': '#00b100'})
                    count +=1

    print("print edges")
    print(edges)
    graph_objects ={"nodes":nodes,"edges": edges}

    return graph_objects

def returnNormalizedCount(value1, value2):
    return int(value1/value2 *10)

app.jinja_env.globals.update(returnNormalizedCount=returnNormalizedCount)

# Path to render the html to display the search page
@app.route('/')
def displaySearch():
    print("placeholder")

    query = db.returnUniqueQueryValues()
    queryDict = { i : None for i in query } #format into dict format

    print(queryDict)

    directory = db2.returnDirectory()

    return render_template('landingpage.html', searchValues=queryDict,directory = directory)


# path to render the results page.  the searchQuery parameter is passed from the landing page.
@app.route('/result/<searchQuery>')
def diplayresult(searchQuery):
    print("placeholder2")
    data = db.returnKeywordValues(searchQuery)
    print(data)
    graph = buildGraph(data["all"])



    return render_template('results2.html', searchQuery=searchQuery, data=data["all"], verbs =data["verbs"], nouns = data["nouns"], adjectives = data["adjectives"], adverbs = data["adverbs"], high_keyword = data["high_keyword"],   nodes=graph['nodes'], edges=graph['edges'])

@app.route('/test')
def test():
        return "I Work!!!!"

# run flask app
if __name__ == '__main__':

    #print(read_file('text_save.txt'))

    app.run()

