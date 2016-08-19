import unittest
from template1 import Template
from exceptions import TemplateError

class TemplateTest(unittest.TestCase):
    def testText(self):
        data = {
            'var1': 'var1',
            'var2': 'var2',
            'list': [
                {'var3': 'var3_1'},
                {'var3': 'var3_2'},
                {'var3': 'var3_3'},
                {'var3': 'var3_4'},
            ],
        }
        tmpl = Template(text="""
        text
        text
        text""")
        text1 = tmpl.render(data)
        text2 = b'text text text'
        self.assertEqual(text1, text2)

    def testVal(self):
        data = {
            'var1': 'var1',
            'var2': 'var2',
            'list': [
                {'var3': 'var3_1'},
                {'var3': 'var3_2'},
                {'var3': 'var3_3'},
                {'var3': 'var3_4'},
            ],
        }
        tmpl = Template(text="""
        text
        {{var1}}
        text
        {{var2}}
        text""")
        text1 = tmpl.render(data)
        text2 = b'textvar1textvar2text'
        self.assertEqual(text1, text2)

    def testIf(self):
        data = {
            'var1': 'var1',
            'var2': 'var2',
            'list': [
                {'var3': 'var3_1'},
                {'var3': 'var3_2'},
                {'var3': 'var3_3'},
                {'var3': 'var3_4'},
            ],
        }
        tmpl = Template(text="""
        {% if var1 == var1: %}
        {{var1}}
        {% end %}
        {% if var2 != var2: %}
        {{var1}}
        {% else %}
        {{var2}}
        {% end %}
        {% if var1 == test: %}
        {{var1}}
        {% else %}
        {{var2}}
        {% end %}
        {% if var1 != test: %}
        {{var1}}
        {% else %}
        {{var2}}
        {% end %}
        {% else %}
        {{var2}}
        {% end %}
        """)
        text1 = tmpl.render(data)
        text2 = b'var1var2var2var1'
        self.assertEqual(text1, text2)

    def testFor(self):
        data = {
            'var1': 'var1',
            'var2': 'var2',
            'list': [
                {'var3': 'var3_1'},
                {'var3': 'var3_2'},
                {'var3': 'var3_3'},
                {'var3': 'var3_4'},
            ],
        }
        tmpl = Template(text="""
        text
        {{var1}}
        text
        {{var2}}
        text
        {% for item in list:%}
        {{item.var3}}
        {% end %}""")
        text1 = tmpl.render(data)
        text2 = b'textvar1textvar2textvar3_1var3_2var3_3var3_4'
        self.assertEqual(text1, text2)

    def testForFor(self):
        data = {
            'var1': 'var1',
            'var2': 'var2',
            'list2': [
                {'var3': [{'var4': 'var4_1_1'}, {'var4': 'var4_1_2'}, {'var4': 'var4_1_3'}]},
                {'var3': [{'var4': 'var4_2_1'}, {'var4': 'var4_2_2'}, {'var4': 'var4_2_3'}]},
                {'var3': [{'var4': 'var4_3_1'}, {'var4': 'var4_3_2'}, {'var4': 'var4_3_3'}]},
            ],
        }
        tmpl = Template(text="""
        {% for list1 in list2:%}
        //-{{var1}}
        {% for list0 in list1.var3:%}
        --
        {{list0.var4}}
        /{{var2}}
        {% end %}
        {% end %}""")
        text1 = tmpl.render(data)
        text2 = b'//-var1--var4_1_1/var2--var4_1_2/var2--var4_1_3/var2//-var1--var4_2_1/var2--var4_2_2/var2--var4_2_3/var2//-var1--var4_3_1/var2--var4_3_2/var2--var4_3_3/var2'
        self.assertEqual(text1, text2)

    def testEnd(self):
        data = {
            'var1': 'var1',
            'var2': 'var2',
            'list': [
                {'var3': 'var3_1'},
                {'var3': 'var3_2'},
                {'var3': 'var3_3'},
                {'var3': 'var3_4'},
            ],
        }
        tmpl = Template(text="""
        {% fot item in list:%}
        {% if var1 == var1: %}
        {{var1}}
        {% end %}
        """)
        text1 = tmpl.render(data)
        text2 = TemplateError('Parce error: unknown block operator {%fot item in list:%}')
        self.assertEqual(text1, text2)



