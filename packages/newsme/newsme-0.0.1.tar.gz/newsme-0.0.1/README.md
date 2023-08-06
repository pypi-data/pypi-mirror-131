# NewsApp
NewsApp package makes interaction with newsApi easier and allows you to create simple html mails.

Features:
* Easy interaction with news api 
* Simple mail setup! Just provide req information and you are ready to go.
* Generate html content from api results in desired form

## What you need to use this app?
* If you are going to use NewApi you need an api key 
* You need an email address to send emails.
## How to use?
* For interaction with newsApi use GetNews class
* For creating html elements use CreateHtml class
* For sending mails use NewsShare class

## Installation
```
git clone https://github.com/lunfman/NewsApp.git
```
## Modules
### GetNews class
GetNesws object provides simple interaction with NewsApI.
```
from get_news import GetNews
news = GetNews('API_KEY')
```

#### Default parameters
* default endpoint is everything_endpoint
```
everything_endpoint = 'https://newsapi.org/v2/everything'
top_headlines_endpoint = 'https://newsapi.org/v2/top-headlines'

# Default endpoint
endpoint = everything_endpoint

# Change endpoint to top_headlines
GetNews.endpoint = GetNews.top_headlines_endpoint
```

* date = today
* search_type = qInTitle -> other options is q -> GetNews.search_type = 'q'
* default parameters for the api request

```        
params = {
            self.search_type: '',
            'from': self.date,
            'sortBy': 'popularity',
            'language': 'en',
            'apiKey': self.API_KEY,
        }
```
* articles_num = 5 'How many articles you wish to get after extractions works with show and get_list methods

#### Methods
##### GetNews.search(keyword)
Method takes one argument -> keyword (what are you searching for?)

Search method interact with the api and save results to api_data and create articles list after execution
```
from get_news import GetNews
news = GetNews('API_KEY')
news.search('github')

# get json data after search
data = news.api_data
# data['articles'] etc..
```

##### GetNews.get_list() 
This method returns a list with articles [article1, article2...]
Use this method after search or it will return an empty list
```
# return a list with articles and sliced by news.article_num value
news.get_list()

```
##### GetNews.show()
Method prints to console all articles in formatted form
```
news.show()
-------------
article source

article title 

article content

article url
```

##### GetNews.new_params(**kwargs)
Method for creating parameters. Check Newsapi documentation for parameters).
* This method overwrites default parameters
* You do not need to provide an api key if you use this method
* If you wish to change search_type change it directly do not create it with this method.

```
news.new_params('date'=date, 'param2':param2)
# Result:
# news.params
{
    'date':date,
    'param2:param2,
    'apiKey':api_key
}
```

### CreateHtml class
Use this class to create an html.
```
from html_creator import CreateHtml
create_html = CreateHtml()
```

#### Methods
##### CreateHtml.simple(**kwargs)
This method creates html tags from kwargs. After execution html will be stored in CreateHtml.html.
```
create_html.simple(h1='heading 1', p='paragraph 1')
create_html.simple(h1='heading 2', p='paragraph 2')
html = create_html.html
----------------------------
# html = '<h1>heading 1</h1><p>paragraph 1</p><h1>heading 2</h1><p>paragraph 2</p>'
```

##### CreateHtml.read_template()
* Use this method if you wish to use your own template. (Works only with very basic templates)
* Inside the template should be placed the next string [CONTENT] which will be replaced after with created html.
* Templates path by default set to /template.html
* The template should have the next name template.html !

```
/template.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
[CONTENT]
</body>
</html>

```

##### CreateHtml.replace_content()
Use method to replace templates [CONTENT] string with current CreateHtml.html
```
# init CreateHtml class
create_html = CreateHtml()
# create a line of html
create_html.simple(h1='heading 1', p='paragraph 1')
# open template -> template will be stored in create_html.template
create_html.reade_template()
# replace [CONTENT] with created html
create_html.replace_content()

-----------------------------------------
#  create_html.template
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1>heading 1</h1><p>paragraph 1</p>
</body>
</html>

```

##### CreateHtml.get()
This method combines two previous methods and returns modified template


### ShareNews Class
ShareNews class allows to prepare html file for sending and send mails to desired destination


While init your need to provide the next parameters
* mail - mail which is going to connect to smtp server for sending mails
* destination - who whill receive message
* password - password for the mail
* smtp_server - smtp server of provider 
```
Example
smtp.gmail.com
smtp-mail.outlook.com
```

Default params:


port = '465'


subject = 'News'

```
from mail import ShareNews
send = ShareNews(
        mail='mail which is going to connect to smtp server',
        password = 'password for this mail',
        smtp_server = 'smtp.gmail.com',
        destination = 'mail@mail.com who will receive the message')
```

### How to add html to the ShareNews class?
```
send.html = 'your html as a string'
```
The plain text can be added the same way.

#### ShareNews.send()
Method for sending an email. Use it when html is added to the class and ready to send an email.


## Examples
Examples demonstrate how to use all pieces together to create an app by using this package.

### Example 1
Get information from NewsApi and send html mail to your destination.
```
from html_creator import CreateHtml
from get_news import GetNews
from mail import ShareNews

topics = ['github', 'microsoft']

key = 'api_key'
news = GetNews(key)
news.articles_num = 1

create_html = CreateHtml()

sender = ShareNews(
   mail='mail',
   password='pass',
   destination='to',
   smtp_server='smtp')

for topic in topics:
   create_html.simple(h1=topic)
   for article in news.search(topic).get_list():
      title = article['title']
      content = article['content']
      create_html.simple(b=title, p=content)
   

sender.html = create_html.html
sender.text = ''

sender.send()
```
### Example 2
Print news to the console
```
from get_news import GetNews

# topics for search
topics = ['github', 'microsoft']

# init GetNews class
news = GetNews('api_key')

# show only two articles
news.articles_num = 2

for topic in topics:
    # search for topic and print news related to the topic
    news.search(topic).show()
```

### Example 3
Use different endpoints and params
```
from get_news import GetNews

news = GetNews('apikey')
# using top headlines endpoint
news.endpoint = news.top_headlines_endpoint
news.new_params(
    country = 'us',
)

news.search('').show()
```

### Example 4
Create html mail and send it
```
from html_creator import CreateHtml
from mail import ShareNews

sender = ShareNews(
    mail='mail',
    password= 'pass',
    destination= 'destination',
    smtp_server= 'server',
    subject= 'subject'
)

html_creator = CreateHtml()
heading = 'Heading of the message'
paragraph = 'Some information'

html_creator.simple(h1=heading, p=paragraph)
# open template and replace [CONTENT] with html
html_creator.get()
# selecting modified template
html = html_creator.template
# adding html to sender
sender.html = html
sender.send()
```

