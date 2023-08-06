from html_creator import CreateHtml
from get_news import GetNews
from mail import ShareNews

topics = ['github']

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

#sender.send()
