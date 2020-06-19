"""
from helper import Helper
from app_settings import AppSettings
import json

class HelperSetClauseFormat(Helper):
    def __init__(self, step=None):
        super().__init__(step)
        self.object_types = ['JSONB']
        self.unquoted_types = ['INTEGER', 'BOOLEAN']
        self.quoted_types = ['TEXT', 'TIMESTAMP']
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

        set_fields = ['{}_{}=_{}'.format(self.dictionary['tbl-prefix'],f['name'], f['name'])
                      for f in self.dictionary['tbl-fields']
                      if f['context'] != 'pk' and 'crud' in f and 'u' in f['crud']]

        #self.lines.append(' and '.join(set_fields))
        self.lines.append('            {}'.format(', '.join(set_fields)))

        return self

def main():
    import pprint
    from test_func import test_table
    import os

    os.environ['LB-TESTING'] = '1'
    lines = HelperSetClauseFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()
"""