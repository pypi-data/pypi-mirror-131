import os

class CreateHtml:

    def __init__ (self):
        # html is going to store extracted html
        self.html = ''
        
        # path for the template
        self.template_path = f'{os.path.dirname(os.path.realpath(__file__))}/template.html'
        
        # store template after read
        self.template = ''

    """
    method create_simple_html
    - accepts **kwargs like h1 = , p = ,a = , b =, i =, and etc
    - you can pass as many params as you wish as strings

    1. Example
    CreateHtml.create_simple_htm(h1 = 'title', p='Text)
    return -----> [<h1>title</h1>,<p>Text</p>]
    The list of converted values will be returned 
    
    """

    def simple(self,**kwargs):
        # this method can create a simple html block by providing html tags and values
        # after completing function saves result to self.html_list as a new list / block
        for key, value in kwargs.items():
            # creating element from key and value
            element = f'<{key}>{value}</{key}>'
            self.html += element

        return self


    def read_template(self):
        # open template
        with open(self.template_path) as html_template:
            template_content = html_template.read()
        self.template = template_content
        return self

    def replace_content(self):
        # method replace templates content with created_html
        # what if [content] not in the file ?!
        self.template = self.template.replace('[CONTENT]', self.html)
        return self


    def get(self):
        # get -> open template / 
        # replace content with html / return modifed template
        self.read_template()
        self.replace_content()
        return self.template