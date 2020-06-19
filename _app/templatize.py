"""
#from helper import Helper
from app_settings import AppSettings
import json

class dep_TemplatizedLine(list):
    '''
    Merges a single template line with configuration values
    '''
    def __init__(self, dictionary, template_line):
        self.dictionary = dictionary
        self.template_line = template_line
        self.process()

    def process(self):
        if '[[' in self.template_line :
            for key_ in self.dictionary:
                v = self.dictionary[key_]
                if type(v) != list and type(v) != dict:
                    #print('process key', key_, ' v ', v)
                    self.template_line = self.template_line.replace('[[{}]]'.format(key_), v)

        self.append(self.template_line)

        return self

class dep_Templatize(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.lines=[]
        self.template=None

    def set_dictionary(self, table_dictionary):
        self.dictionary = table_dictionary
        return self

    def set_template(self, template):
        self.template = template
        return self

    def templatize(self,template):
        self.set_template(template)
        self.process()
        return self.lines[0]

    def process(self):
        # tempatize
        #print('process', self.dictionary)
        for key_ in self.dictionary:
            v = self.dictionary[key_]
            if type(v) != list and type(v) != dict:
                #print('process key', key_, ' v ', v)
                self.template = self.template.replace('[[{}]]'.format(key_), v)
        self.lines.append(self.template)
        return self


def main():
    from test_func import test_table

    import pprint
    import os

    os.environ['LB-TESTING'] = '1'

    tmpl = Templatize().set_dictionary(test_table()).templatize('im a little ([[tbl-name]]) template ')
    assert (type(tmpl)==str) # is a list
    print(tmpl)

    tmpl = Templatize()\
        .set_dictionary(test_table()['tbl-fields'][0])\
        .templatize('im a [[tbl-prefix]] little ([[name]]) template ')
    assert (type(tmpl) == str)  # is a list
    print(tmpl)

    print('TemplatizedLine', TemplatizedLine(test_table(),'passthrough'))
    assert TemplatizedLine(test_table(),'passthrough') == ['passthrough']
    assert TemplatizedLine(test_table(),'[[tbl-name]]') == ['register']

    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
"""