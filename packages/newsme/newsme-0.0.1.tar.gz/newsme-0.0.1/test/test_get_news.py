from typing import NewType
import unittest
from unittest import mock
from unittest.mock import patch
import json
from newsme.get_news import GetNews
import os

path = f'{os.path.dirname(os.path.realpath(__file__))}/data.json'
with open(path) as json_file:
    data = json.load(json_file)

news_api_error = {"status":"error","code":"apiKeyMissing","message":"Your API key is missing. Append this to the URL with the apiKey param, or use the x-api-key HTTP header."}


class TestGetNewsClass(unittest.TestCase):
    
    def setUp(self):
        self.news = GetNews('api key')
        self.news.api_data = data
        

    def test_get_list(self):
        # pretending that data already exists
        # news.api_data = data!
        # and creating articles! normally created inside of news.search method
        self.news.articles_num = 2
        self.news.articles = self.news.api_data['articles'][:self.news.articles_num]
        self.assertLessEqual(len(self.news.get_list()), 2)

        self.news.articles_num = 1
        self.news.articles = self.news.api_data['articles'][:self.news.articles_num]
        self.assertLessEqual(len(self.news.get_list()), 1)

    def test_new_params(self):
        self.assertEqual(self.news.new_params(language='a', date = 'b').params,
            {'language':'a', 'date':'b', 'apiKey': 'api key'})

        # what to do if user adds q/qintitle with keyword???!!
        # right now using search_type! think about it!
        self.assertEqual(self.news.new_params(q='a', date = 'b').params,
            {'q':'a', 'date':'b', 'apiKey': 'api key'})

    @patch('newsme.get_news.requests.get')
    def test_search(self, mock_get):

        # get 1 article in articles
        self.news.articles_num = 1
        # json = data
        mock_get.return_value.json.return_value = data
        # articles len == 1 
        self.assertEqual(len(self.news.search('tesla').articles), 1)

        # api return not ok -> dealing with api problem
        mock_get.return_value.json.return_value = news_api_error
       
        with self.assertRaises(Exception) as context:
            self.news.search('test')
        expected_error = ('apiKeyMissing', 'Your API key is missing. Append this to the URL with the apiKey param, or use the x-api-key HTTP header.')
        self.assertTrue(str(expected_error) == str(context.exception))
        
        # new request
        mock_get.return_value.json.return_value = data
        self.news.search('tesla')
        # api_data = json from response
        self.assertEqual(self.news.api_data, data)
        # get 3 articles will not work!!! because slice inside of search method
        self.news.articles_num = 3
        # the list equal to 3 based on data
        self.assertEqual(len(self.news.get_list()), 1)
        # new search with articles_num  = 3 and now it should
        # be = to 3!!
        self.news.search('tesla')
        self.assertEqual(len(self.news.get_list()), 3)


if __name__ == '__main__':
    unittest.main()