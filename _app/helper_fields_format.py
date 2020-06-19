"""
from helper import Helper
from app_settings import AppSettings
import json
from templatize import Templatize

class dep_HelperFieldsFormat(Helper):
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
        #print('context',self.getContext())
        temp = [Templatize()
                  .set_dictionary(f)
                  .templatize(self.getContext()[f['context']])
              for f in FieldList(self.dictionary)
            ]
        '''
        temp = [Templatize()
                  .set_dictionary(f)
                  .templatize(self.getContext()[f['context']])
              for f in self.dictionary['fields']
              if 'crud' in f and len(f['crud']) > 0
            ]
        '''
        self.lines.append('    {}'.format(',\n    '.join(temp)) )

        return self



def main():
    import pprint
    from test_func import test_table

    import os
    os.environ['LB-TESTING'] = '1'
    lines = dep_HelperFieldsFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list
    print('lines', lines)
    #pprint.pprint(lines)
    #print(',\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
"""