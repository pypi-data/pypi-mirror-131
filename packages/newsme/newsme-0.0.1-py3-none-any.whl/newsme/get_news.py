try:
    import requests
except ModuleNotFoundError:
    # for vscode
    import pip._vendor.requests as requests

import datetime
# API Ref
"""
qInTitle - Keywords or phrases to search for in the article title only.
q - Keywords or phrases to search for in the article title and body.

sortBy
The order to sort the articles in. Possible options: relevancy, popularity, publishedAt.
relevancy = articles more closely related to q come first.
popularity = articles from popular sources and publishers come first.
publishedAt = newest articles come first.
"""

class GetNews:

    def __init__(self, api_key):
        # api key and endpoints
        self.API_KEY = api_key
        self.everything_endpoint = 'https://newsapi.org/v2/everything'
        self.top_headlines_endpoint = 'https://newsapi.org/v2/top-headlines'
        
        # default endpont 
        self.endpoint = self.everything_endpoint
        
        # dates
        self.today = datetime.datetime.today().date()   
        # date by default is today
        self.date = self.today

        # search type by default keyword in title
        self.search_type = 'qInTitle'
        # default parameters
        # two options for changeing it first by changeing it manually -> class.paramas = {params}
        # or by using create_params method
        self.params = {
            self.search_type: '',
            'from': self.date,
            'sortBy': 'popularity',
            'language': 'en',
            'apiKey': self.API_KEY,
        }
        
        # number of articles by deafault
        self.articles_num = 5
        
        # stores api response in json format
        self.api_data = ''
        # store extracted articles after successfull search
        self.articles = []


    def new_params(self, **kwargs):
        # overwrite existing parameters
        self.params = {}
        
        for key, value in kwargs.items():
            self.params[key] = value

        # add api key after new params was created
        self.params['apiKey'] = self.API_KEY
        
        return self
   

    def search(self, keyword):
        # add keyword to params
        self.params[self.search_type] = keyword

        self.response = requests.get(self.endpoint, params=self.params)
        self.api_data = self.response.json()
        if self.api_data['status'] != 'ok':
           self.response_errors()

        # if all good extract articles array from api data for forward use
        self.articles = self.api_data['articles'][:self.articles_num]
        
        return self


    def get_list(self):
        # return a list with articles from articles
        # use after get_everything method
        return [article for article in self.articles]


    def show(self):
        # this method just prints the news in formated way
        news = ''
        # looping through api data and extracting news
        # articles = api_data[articles]and slice this list by articles num
        
        for article in self.articles:
            article_source = article['source']['name']
            article_title = article['title']
            article_content = article['content']
            article_url = article['url']
            news += f"{article_source}\n{article_title}\n{article_content}\n{article_url}\n\n" 
        print(news)
        return self
    
    
    def response_errors(self):
        code = self.api_data['code']
        mesage =  self.api_data['message']
        raise Exception (code, mesage)       