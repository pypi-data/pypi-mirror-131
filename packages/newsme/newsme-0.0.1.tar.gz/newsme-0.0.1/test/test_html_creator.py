from re import I, S
import unittest
from newsme.html_creator import CreateHtml
import os

class TestCreateHtmlClass(unittest.TestCase):

    def setUp(self):
        self.html_creator = CreateHtml()

    def test_simple_method(self):
        # test 1 creating tags
        self.assertEqual(self.html_creator.simple(h1='test1', b = 'test1', p = 'test1').html,
            '<h1>test1</h1><b>test1</b><p>test1</p>')
        
        self.html_creator.html = ''
        # test 2 creating wired tags
        self.assertEqual(self.html_creator.simple(test='test').html,
            '<test>test</test>')
        # test 3 creating one more -> should be added to the last
        self.assertEqual(self.html_creator.simple(p='test').html,
            '<test>test</test><p>test</p>')
        

    def test_read_template(self):
        # file do not exists
        self.html_creator.template_path =  f'{os.path.dirname(os.path.realpath(__file__))}/templatee.html'
        with self.assertRaises(FileNotFoundError) as context:
            self.html_creator.read_template()
        # file not found error
        self.assertTrue('[Errno 2]' in str(context.exception))
    
    def test_replace_content(self):
        # test 1 [CONTENT] not in template.html
        self.html_creator.html = '<h1>test1</h1><b>test1</b><p>test1</p>'
        self.test_temp = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body></body></html>'
        # nothing should change because [CONTENT] not in file   
        self.html_creator.template = self.test_temp
        self.html_creator.replace_content()
        self.assertEqual(self.test_temp, self.test_temp)
        

        # test 2 [CONTENT] exists
        self.html_creator.template = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body>[CONTENT]</body></html>'
        self.html_creator.html = '<h1>test1</h1><b>test1</b><p>test1</p>'
        expected = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body><h1>test1</h1><b>test1</b><p>test1</p></body></html>'
        self.html_creator.replace_content()
        self.assertEqual(self.html_creator.template, expected)

if __name__ == '__main__':
    unittest.main()