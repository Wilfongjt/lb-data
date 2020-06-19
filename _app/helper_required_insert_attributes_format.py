"""
from helper import Helper
from app_settings import AppSettings
from list_fields import FieldList
class HelperRequiredInsertAttributesFormat(Helper):
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

        #required_attributes = ['_json ? \'{}\''.format( f['name']) for f in self.dictionary['tbl-fields'] if 'json' in f and 'c' in f['json']]
        #required_attributes = ['_json ? \'{}\''.format( f['name']) for f in FieldList(self.dictionary,['c']) self.dictionary['tbl-fields'] if 'crud' in f and 'c' in f['crud']]
        required_attributes = ['_json ? \'{}\''.format( f['name']) for f in FieldList(self.dictionary,['C'])]

        if len(required_attributes) == 0:
            self.lines('    /* No required attribute configured.  Add \'c\' to crud. */')
        else:

            self.lines.append('    not (')
            self.lines.append(' and '.join(required_attributes))
            self.lines.append('    )')

        return self

def main():
    from test_func import test_table
    import os

    import pprint
    os.environ['LB-TESTING'] = '1'
    lines = HelperRequiredInsertAttributesFormat().set_dictionary(test_table()).format()

    assert (type(lines)==list) # is a list

    #pprint.pprint(lines)
    print('\n'.join(lines))
    os.environ['LB-TESTING'] = '0'
if __name__ == "__main__":
    main()
"""