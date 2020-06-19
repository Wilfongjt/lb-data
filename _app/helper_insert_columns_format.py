"""
from helper import Helper
from app_settings import AppSettings
import json
from list_fields import FieldList

class depHelperInsertColumnsFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)

        self.dictionary = None
        self.lines=[]

    def set_dictionary(self, table_dictionary ):
        self.dictionary = table_dictionary
        return self

    def format(self):

        self.process()

        return self.lines

    def process(self):
        # tempatize
        if self.dictionary == None:
            raise Exception('Table Dictionary is not set!')

        field_names = ['{}_{}'.format(self.dictionary['tbl-prefix'], f['name'])
                       for f in FieldList(self.dictionary,['c','C'])]

        self.lines.append('                {}'.format(', '.join(field_names)))
        return self

def main():
    import pprint
    from test_func import test_table
    import os

    os.environ['LB-TESTING'] = '1'
    helper = HelperInsertColumnsFormat().set_dictionary(test_table())
    #print('tbl-fields',[f['name'] for f in helper.getFields()])
    #assert [f['name'] for f in helper.getFields()] == ['type','password','attributes']

    lines = helper.format()
    assert (type(lines)==list) # is a list
    assert lines == ['                reg_type, reg_form, reg_password']
    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
"""