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