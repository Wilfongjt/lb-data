"""
from helper import Helper
from app_settings import AppSettings
import json
from list_fields import FieldList

class depHelperInsertValuesFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.dictionary = None
        self.lines=[]

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self
    ''' 
    def getFields(self):
        return [f for f in self.dictionary['fields']
                if 'crud' in f
                and ('c' in f['crud'] or 'C' in f['crud'])]
    '''
    def format(self):

        self.process()

        return self.lines

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        #field_values = ['_{}'.format(f['name'])
        #                for f in self.dictionary['fields'] if 'crud' in f and 'c' in f['crud']]

        field_values = ['_{}'.format(f['name'])
                        for f in FieldList(self.dictionary, ['c','C','F'])]

        self.lines.append('                {}'.format(', '.join(field_values)))

        return self

def main():
    import pprint
    from test_func import test_table
    import os
    os.environ['LB-TESTING'] = '1'
    helper = HelperInsertValuesFormat().set_dictionary(test_table())

    #print('fields', [f['name'] for f in FieldList()])
    #assert [f['name'] for f in helper.getFields()] == ['type', 'password', 'attributes']

    lines = helper.format()
    assert (type(lines)==list) # is a list
    #print('lines', lines)
    assert lines == ['                _type, _form, _password']
    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
"""