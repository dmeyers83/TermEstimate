from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from gensim.parsing.preprocessing import remove_stopwords

class prototypeScrapper:
    # create a webdriver object and set options for headless browsing
    options = Options()
    options.headless = True
    browser = webdriver.Chrome('./chromedriver', options=options)

    allLinks = []  # list to capture
    page_data_list = []  # list of all docuemnts

    def __init__(self, q='Python Developer', l='New+York+State'):
        self.run_indeed_query(q,l)
        return self.scrape_pages()

    # uses webdriver object to execute javascript code and get dynamically loaded webcontent
    def get_js_soup(self, url, browser):
        browser.get(url)
        res_html = browser.execute_script('return document.body.innerHTML')
        soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
        return soup

    # tidies extracted text
    def process_text(self, text):
        text = text.encode('ascii', errors='ignore').decode('utf-8')  # removes non-ascii characters
        text = re.sub('\s+', ' ', text)  # repalces repeated whitespace characters with single space
        return text

    ''' More tidying
    Sometimes the text extracted HTML webpage may contain javascript code and some style elements. 
    This function removes script and style tags from HTML so that extracted text does not contain them.
    '''

    def remove_script(self, soup):
        for script in soup(["script", "style"]):
            script.decompose()
        return soup

    # helper function to write lists to files
    def write_lst(lst, file_):
        with open(file_, 'w') as f:
            for l in lst:
                f.write(l)
                f.write('\n')

    def read_list(file):
        f = open(file, 'r')
        return f.readlines()

    def scrape_search_result_page(self,dir_url, page_result, browser):
        print('-' * 20, 'Scraping indeed search result page ' + str(page_result) + '', '-' * 20)
        indeed_links = []
        # execute js on webpage to load faculty listings on webpage and get ready to parse the loaded HTML
        soup = self.get_js_soup(dir_url, browser)
        for link_holder in soup.find_all('div', class_='title'):  # get list of all <div> of class 'photo nocaption'
            rel_link = link_holder.find('a')['href']  # get url
            # url returned is relative, so we need to add base url
            if rel_link != '':
                indeed_links.append('https://www.indeed.com' + rel_link)
        print('-' * 20, 'Found {} indeed search urls'.format(len(indeed_links)), '-' * 20)
        return indeed_links

    def run_indeed_query(self, q='Python Developer', l='New+York+State'):
        start = 0  # pagnigation variable, page 1 = 0, page 2 = 10, page 3 = 30, etc
        numPage = 20  # num pages to scrap links from

        for page_result in range(numPage):
            start = page_result * 10  # increment the variable used to denote the next page
            search_result_url = 'https://www.indeed.com/jobs?q=' + q + '&l=' + l + '&start=' + str(start)  # build query string
            print(search_result_url)
            jobSearchResult = self.scrape_search_result_page(search_result_url, page_result, self.browser)  # call scraper function
            self.allLinks.extend(jobSearchResult)  # add to link

    def scrape_pages(self):
        homepage_found = False
        page_data = ''
        for indeed_url in self.allLinks:
            try:
                page_soup = self.remove_script(self.get_js_soup(indeed_url, self.browser))
            except:
                print('Could not access {}'.format(indeed_url))

            page_data = self.process_text(page_soup.get_text(separator=' '))  # helper function hw to clean up text

            # remove header
            page_data = page_data[189:]  # the 189 slice removes the header of the indeed pages

            # remove footer
            footer_position = page_data.find('save job')  # find the position of 'save job' which starts the footer
            trimStringBy = footer_position - len(page_data)  # returns a negative number to trim the string by
            page_data = page_data[:trimStringBy]  # drop footer
            page_data = remove_stopwords(page_data)
            self.page_data_list.append(page_data)